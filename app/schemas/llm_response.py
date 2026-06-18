"""LLM response Pydantic schemas."""

from pydantic import BaseModel, ConfigDict


class LLMResponseRead(BaseModel):
    """LLM benchmark response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If data is invalid.
    """

    id: int
    run_id: int
    status: str
    word_count: int
    pv_count: int
    pvr_per_1k: float
    output_text: str
    model_config = ConfigDict(from_attributes=True)
