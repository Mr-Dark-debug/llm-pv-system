"""LLM model Pydantic schemas."""

from pydantic import BaseModel, ConfigDict


class LLMModelRead(BaseModel):
    """LLM model response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If data is invalid.
    """

    id: int
    model_id: str
    provider: str
    display_name: str
    pvr_overall: float
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
