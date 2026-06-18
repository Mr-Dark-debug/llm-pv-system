"""JSON benchmark API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import LLMModel
from app.schemas.llm_model import LLMModelRead
from app.services.benchmark_runner import BenchmarkRunner

router = APIRouter(prefix="/api/benchmark", tags=["benchmark"])


@router.get("/models", response_model=list[LLMModelRead])
async def list_models(db: Session = Depends(get_db)) -> list[LLMModel]:
    """List benchmarked LLMs.

    Args:
        db: Database session dependency.

    Returns:
        list[LLMModel]: Model rows.

    Raises:
        None.
    """

    return db.query(LLMModel).order_by(LLMModel.display_name).all()


@router.post("/run/{model_id}")
async def run_benchmark(model_id: int, prompt_limit: int | None = None, db: Session = Depends(get_db)) -> dict:
    """Run benchmark for one model.

    Args:
        model_id: Model primary key.
        prompt_limit: Optional prompt cap.
        db: Database session dependency.

    Returns:
        dict: Benchmark summary.

    Raises:
        HTTPException: If the model does not exist.
    """

    try:
        return await BenchmarkRunner(db).run_model(model_id, prompt_limit=prompt_limit)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
