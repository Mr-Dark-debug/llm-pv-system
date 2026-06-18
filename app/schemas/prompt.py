"""Prompt Pydantic schemas."""

from pydantic import BaseModel, ConfigDict


class PromptRead(BaseModel):
    """Benchmark prompt response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If data is invalid.
    """

    id: int
    prompt_id: str
    prompt_type: str
    prompt_text: str
    target_pv: str | None = None
    expected_register: str
    model_config = ConfigDict(from_attributes=True)
