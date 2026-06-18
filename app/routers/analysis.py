"""JSON analysis API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.get("/summary")
async def analysis_summary(db: Session = Depends(get_db)) -> dict:
    """Return statistical analysis summary.

    Args:
        db: Database session dependency.

    Returns:
        dict: Analysis summary payload.

    Raises:
        None.
    """

    return AnalysisService(db).summary()
