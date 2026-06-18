"""Admin JSON API routes."""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.export_service import ExportService

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/export/participants.csv")
async def export_participants_csv(db: Session = Depends(get_db)) -> Response:
    """Export participants and scores as CSV.

    Args:
        db: Database session dependency.

    Returns:
        Response: CSV response.

    Raises:
        csv.Error: If serialization fails.
    """

    return Response(ExportService(db).participants_csv(), media_type="text/csv")


@router.get("/export/benchmark.json")
async def export_benchmark_json(db: Session = Depends(get_db)) -> Response:
    """Export benchmark responses as JSON.

    Args:
        db: Database session dependency.

    Returns:
        Response: JSON response.

    Raises:
        TypeError: If serialization fails.
    """

    return Response(ExportService(db).benchmark_json(), media_type="application/json")
