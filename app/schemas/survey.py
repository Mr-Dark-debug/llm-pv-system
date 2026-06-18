"""Survey request and response schemas."""

from pydantic import BaseModel, Field


class SurveySubmit(BaseModel):
    """Survey submission request schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If payload data is invalid.
    """

    study: str = Field(pattern="^study[12]$")
    condition: str | None = None
    survey_link_token: str | None = None
    demographics: dict = Field(default_factory=dict)
    usage: dict = Field(default_factory=dict)
    tasks: dict = Field(default_factory=dict)
    qualitative: dict = Field(default_factory=dict)


class SurveySubmitResponse(BaseModel):
    """Survey submission response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If payload data is invalid.
    """

    participant_code: str
    lei: float | None
    pva: float | None


class SurveyLinkCreate(BaseModel):
    """Survey link creation request schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If payload data is invalid.
    """

    study: str = Field(pattern="^study[12]$")
    label: str = "Research survey link"
    condition: str | None = None


class SurveyLinkRead(BaseModel):
    """Survey link response schema.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If payload data is invalid.
    """

    token: str
    study: str
    label: str
    condition: str | None = None
    is_active: bool
    response_count: int
    url: str | None = None
