"""Survey administration and scoring service."""

from sqlalchemy.orm import Session

from app.database import utc_now
from app.models import AcceptabilityResponse, ForcedChoiceResponse, LLMModel, Participant, SurveyResponse, TranslationResponse
from app.services.lei_calculator import LEICalculator
from app.services.pva_calculator import PVACalculator
from app.services.survey_link_service import SurveyLinkService


class SurveyService:
    """Persist participant submissions and compute registered scores.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the survey service.

        Args:
            db: SQLAlchemy session.

        Returns:
            None.

        Raises:
            None.
        """

        self.db = db
        self.lei_calculator = LEICalculator()
        self.pva_calculator = PVACalculator()

    def submit_response(
        self,
        study: str,
        demographics: dict,
        usage: dict,
        tasks: dict,
        qualitative: dict,
        condition: str | None = None,
        survey_link_token: str | None = None,
    ) -> tuple[Participant, SurveyResponse]:
        """Create a participant and survey submission.

        Args:
            study: Study identifier.
            demographics: Demographic field values.
            usage: LLM usage field values.
            tasks: Forced-choice, translation, and acceptability responses.
            qualitative: Open-ended responses.
            condition: Optional Study 1 condition.
            survey_link_token: Optional protected survey link token.

        Returns:
            tuple[Participant, SurveyResponse]: Persisted participant and survey rows.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If persistence fails.
        """

        link_service = SurveyLinkService(self.db)
        if survey_link_token:
            link = link_service.get_active(survey_link_token)
            if link is None or link.study != study:
                raise ValueError("Invalid or inactive survey link.")
            condition = link.condition or condition

        participant = Participant(
            participant_code=self._next_participant_code(),
            study=study,
            condition=condition,
            consented_at=utc_now(),
            submission_timestamp=utc_now(),
            age=demographics.get("age"),
            gender=demographics.get("gender"),
            l1_language=demographics.get("l1_language"),
            l1_family=demographics.get("l1_family"),
            other_languages=demographics.get("other_languages"),
            country=demographics.get("country"),
            education=demographics.get("education"),
            years_english=demographics.get("years_english"),
            cefr_self_rating=demographics.get("cefr_self_rating"),
            opt_score=demographics.get("opt_score"),
            attention_checks_passed=demographics.get("attention_checks_passed", 0),
            duration_minutes=demographics.get("duration_minutes"),
        )
        self.db.add(participant)
        self.db.flush()

        forced_choice = tasks.get("forced_choice", [])
        translation = tasks.get("translation", [])
        acceptability = tasks.get("acceptability", [])
        for item in forced_choice:
            self.db.add(ForcedChoiceResponse(participant_id=participant.id, item_id=item["item_id"], pv_chosen=bool(item.get("pv_chosen"))))
        for item in translation:
            self.db.add(
                TranslationResponse(
                    participant_id=participant.id,
                    item_id=item["item_id"],
                    translated_text=item.get("translated_text"),
                    pv_used=bool(item.get("pv_used")),
                    meaning_correct=bool(item.get("meaning_correct")),
                    score=int(item.get("score", 0)),
                    annotator_id=item.get("annotator_id"),
                )
            )
        for item in acceptability:
            self.db.add(
                AcceptabilityResponse(
                    participant_id=participant.id,
                    item_id=item["item_id"],
                    rating=int(item.get("rating", 3)),
                    pv_variant=bool(item.get("pv_variant", True)),
                )
            )

        noticing_values = [value for value in [usage.get("noticing_c7"), usage.get("noticing_c10")] if value is not None]
        noticing_score = sum(noticing_values) / len(noticing_values) if noticing_values else None
        lei = self._calculate_lei(usage)
        pva = self.pva_calculator.calculate(
            forced_choice_pv_chosen=[bool(item.get("pv_chosen")) for item in forced_choice],
            translation_pv_used=[bool(item.get("pv_used")) for item in translation],
            acceptability_scores=[int(item.get("rating", 3)) for item in acceptability],
        )
        survey = SurveyResponse(
            participant_id=participant.id,
            study=study,
            llm_tools_used="|".join(self._tools_used(usage)),
            chatgpt_frequency=int(usage.get("chatgpt_frequency", 1)),
            chatgpt_models="|".join(usage.get("chatgpt_models", [])),
            claude_frequency=int(usage.get("claude_frequency", 1)),
            claude_models="|".join(usage.get("claude_models", [])),
            gemini_frequency=int(usage.get("gemini_frequency", 1)),
            gemini_models="|".join(usage.get("gemini_models", [])),
            copilot_frequency=int(usage.get("copilot_frequency", 1)),
            deepl_frequency=int(usage.get("deepl_frequency", 1)),
            perplexity_frequency=int(usage.get("perplexity_frequency", 1)),
            other_llm_frequency=int(usage.get("other_llm_frequency", 1)),
            other_llm_names=usage.get("other_llm_names"),
            daily_minutes_llm=int(usage.get("daily_minutes_llm", 0)),
            duration_of_use_months=int(usage.get("duration_of_use_months", 1)),
            purpose_grammar=bool(usage.get("purpose_grammar")),
            purpose_vocab=bool(usage.get("purpose_vocab")),
            purpose_translation=bool(usage.get("purpose_translation")),
            purpose_writing=bool(usage.get("purpose_writing")),
            purpose_conversation=bool(usage.get("purpose_conversation")),
            purpose_reading=bool(usage.get("purpose_reading")),
            purpose_pronunciation=bool(usage.get("purpose_pronunciation")),
            noticing_c7=usage.get("noticing_c7"),
            noticing_c8=bool(usage.get("noticing_c8")),
            noticing_c10=usage.get("noticing_c10"),
            noticing_score=noticing_score,
            qualitative_g1=qualitative.get("qualitative_g1"),
            qualitative_g2=qualitative.get("qualitative_g2"),
            lei=lei,
            pva=pva,
        )
        self.db.add(survey)
        link_service.mark_response(survey_link_token)
        self.db.commit()
        self.db.refresh(participant)
        self.db.refresh(survey)
        return participant, survey

    def _calculate_lei(self, usage: dict) -> float:
        """Calculate LEI from persisted benchmark PVR values.

        Args:
            usage: LLM usage values.

        Returns:
            float: LEI score.

        Raises:
            None.
        """

        model_pvrs = {model.model_id: model.pvr_overall for model in self.db.query(LLMModel).all()}
        # Seeded models start with zero; neutral fallback keeps surveys scorable before benchmarks run.
        model_pvrs = {key: (value if value > 0 else 10.0) for key, value in model_pvrs.items()}
        return self.lei_calculator.calculate(
            frequencies={
                "chatgpt": int(usage.get("chatgpt_frequency", 1)),
                "claude": int(usage.get("claude_frequency", 1)),
                "gemini": int(usage.get("gemini_frequency", 1)),
            },
            tool_model_ids={
                "chatgpt": usage.get("chatgpt_models", []),
                "claude": usage.get("claude_models", []),
                "gemini": usage.get("gemini_models", []),
            },
            model_pvrs=model_pvrs,
            duration_of_use_months=int(usage.get("duration_of_use_months", 1)),
            daily_minutes_llm=int(usage.get("daily_minutes_llm", 0)),
        )

    def _tools_used(self, usage: dict) -> list[str]:
        """Infer pipe-delimited tool list from frequency fields.

        Args:
            usage: LLM usage values.

        Returns:
            list[str]: Tool names used more than never.

        Raises:
            None.
        """

        return [tool for tool in ["chatgpt", "claude", "gemini", "copilot", "deepl", "perplexity"] if int(usage.get(f"{tool}_frequency", 1)) > 1]

    def _next_participant_code(self) -> str:
        """Generate the next anonymous participant code.

        Args:
            None.

        Returns:
            str: Code like P00042.

        Raises:
            None.
        """

        next_id = (self.db.query(Participant).count() or 0) + 1
        return f"P{next_id:05d}"
