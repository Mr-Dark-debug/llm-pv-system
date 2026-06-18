"""Participant Pydantic schemas."""

from pydantic import BaseModel, ConfigDict


class ParticipantRead(BaseModel):
    """Participant response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If data is invalid.
    """

    id: int
    participant_code: str
    study: str
    condition: str | None = None
    model_config = ConfigDict(from_attributes=True)
