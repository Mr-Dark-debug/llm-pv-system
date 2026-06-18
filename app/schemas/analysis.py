"""Analysis Pydantic schemas."""

from pydantic import BaseModel


class AnalysisSummary(BaseModel):
    """Analysis summary response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If payload data is invalid.
    """

    counts: dict
    lei_pva_correlation: dict
    model_pvr: list[dict]
    survey_points: list[dict]
