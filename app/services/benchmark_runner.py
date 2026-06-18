"""Benchmark orchestration service."""

from datetime import date

from sqlalchemy.orm import Session

from app.models import LLMModel, LLMResponse, Prompt, PVDetection
from app.services.llm_client import LLMClient
from app.services.pv_detector import PVDetector


class BenchmarkRunner:
    """Run model/prompt benchmark generations and PV detection.

    Args:
        db: SQLAlchemy session.
        llm_client: Optional LLM client.
        pv_detector: Optional PV detector.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, db: Session, llm_client: LLMClient | None = None, pv_detector: PVDetector | None = None) -> None:
        """Initialize the benchmark runner.

        Args:
            db: SQLAlchemy session.
            llm_client: Optional LLM client.
            pv_detector: Optional PV detector.

        Returns:
            None.

        Raises:
            None.
        """

        self.db = db
        self.llm_client = llm_client or LLMClient()
        self.pv_detector = pv_detector or PVDetector()

    async def run_model(self, model_pk: int, run_count: int = 3, prompt_limit: int | None = None) -> dict[str, int | float | str]:
        """Run the benchmark for one model.

        Args:
            model_pk: Primary key of the LLM model.
            run_count: Independent runs per prompt.
            prompt_limit: Optional prompt cap for smoke tests.

        Returns:
            dict[str, int | float | str]: Summary metrics.

        Raises:
            ValueError: If the model id is unknown.
        """

        model = self.db.get(LLMModel, model_pk)
        if model is None:
            raise ValueError(f"Unknown model primary key: {model_pk}")
        prompts_query = self.db.query(Prompt).order_by(Prompt.prompt_id)
        prompts = prompts_query.limit(prompt_limit).all() if prompt_limit else prompts_query.all()
        total = 0
        for prompt in prompts:
            for run_id in range(1, run_count + 1):
                seed = model.id * 100000 + prompt.id * 10 + run_id
                generation = await self.llm_client.generate(model.provider, model.model_id, prompt.prompt_text, seed)
                detection = self.pv_detector.detect(generation.text)
                response = LLMResponse(
                    model_id=model.id,
                    prompt_id=prompt.id,
                    run_id=run_id,
                    seed=seed,
                    output_text=generation.text,
                    word_count=detection.word_count,
                    pv_count=detection.pv_count,
                    pvr_per_1k=detection.pvr_per_1k,
                    generation_date=date.today(),
                    api_latency_ms=generation.latency_ms,
                    api_cost_usd=generation.cost_usd,
                    status=generation.status,
                    error_message=generation.error_message,
                )
                self.db.add(response)
                self.db.flush()
                for item in detection.detections:
                    self.db.add(
                        PVDetection(
                            response_id=response.id,
                            pv_lemma=item.pv_lemma,
                            verb=item.verb,
                            particle=item.particle,
                            sentence_index=item.sentence_index,
                            token_start=item.token_start,
                            token_end=item.token_end,
                            transparency=item.transparency,
                            in_phave_list=item.in_phave_list,
                            layer1_confidence=item.layer1_confidence,
                            annotator1_confirmed=True,
                            final_confirmed=item.final_confirmed,
                        )
                    )
                total += 1
        self._refresh_model_cache(model)
        self.db.commit()
        return {"model_id": model.model_id, "responses_created": total, "pvr_overall": round(model.pvr_overall, 2)}

    def _refresh_model_cache(self, model: LLMModel) -> None:
        """Refresh cached PVR and transparency counts.

        Args:
            model: Model row to update.

        Returns:
            None.

        Raises:
            None.
        """

        responses = self.db.query(LLMResponse).filter(LLMResponse.model_id == model.id).all()
        model.pvr_overall = sum(response.pvr_per_1k for response in responses) / len(responses) if responses else 0.0
        detections = (
            self.db.query(PVDetection)
            .join(LLMResponse, PVDetection.response_id == LLMResponse.id)
            .filter(LLMResponse.model_id == model.id, PVDetection.final_confirmed.is_(True))
            .all()
        )
        model.n_literal_pv = sum(1 for item in detections if item.transparency == "literal")
        model.n_semi_pv = sum(1 for item in detections if item.transparency == "semi_transparent")
        model.n_figurative_pv = sum(1 for item in detections if item.transparency == "figurative")
