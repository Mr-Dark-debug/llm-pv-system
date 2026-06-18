"""Statistical analysis service for benchmark and survey data."""

import json

from scipy import stats
from sqlalchemy.orm import Session

from app.models import LLMModel, Participant, SurveyResponse


class AnalysisService:
    """Run descriptive and inferential analyses.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the analysis service.

        Args:
            db: SQLAlchemy session.

        Returns:
            None.

        Raises:
            None.
        """

        self.db = db

    def summary(self) -> dict:
        """Build dashboard-ready analysis output.

        Args:
            None.

        Returns:
            dict: Descriptive and inferential analysis payload.

        Raises:
            None.
        """

        surveys = self.db.query(SurveyResponse).all()
        models = self.db.query(LLMModel).all()
        lei = [row.lei for row in surveys if row.lei is not None]
        pva = [row.pva for row in surveys if row.pva is not None]
        correlation = self._safe_correlation(lei, pva)
        return {
            "counts": {
                "participants": self.db.query(Participant).count(),
                "survey_responses": len(surveys),
                "models": len(models),
            },
            "lei_pva_correlation": correlation,
            "model_pvr": [{"model": model.display_name, "pvr": round(model.pvr_overall, 2)} for model in models],
            "survey_points": [{"lei": row.lei or 0, "pva": row.pva or 0, "study": row.study} for row in surveys],
        }

    def as_json(self) -> str:
        """Serialize summary results as JSON.

        Args:
            None.

        Returns:
            str: JSON analysis payload.

        Raises:
            TypeError: If values cannot be serialized.
        """

        return json.dumps(self.summary(), default=str, indent=2)

    def _safe_correlation(self, lei: list[float], pva: list[float]) -> dict[str, float | str | None]:
        """Compute Pearson correlation when enough observations exist.

        Args:
            lei: LEI scores.
            pva: PVA scores.

        Returns:
            dict[str, float | str | None]: Correlation result or explanatory status.

        Raises:
            None.
        """

        if len(lei) < 3 or len(pva) < 3 or len(lei) != len(pva):
            return {"status": "insufficient_data", "r": None, "p": None}
        result = stats.pearsonr(lei, pva)
        return {"status": "ok", "r": round(float(result.statistic), 4), "p": round(float(result.pvalue), 4)}
