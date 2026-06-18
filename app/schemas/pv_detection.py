"""PV detection Pydantic schemas."""

from pydantic import BaseModel, ConfigDict


class PVDetectionRead(BaseModel):
    """PV detection response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If data is invalid.
    """

    id: int
    pv_lemma: str
    transparency: str
    final_confirmed: bool
    model_config = ConfigDict(from_attributes=True)
