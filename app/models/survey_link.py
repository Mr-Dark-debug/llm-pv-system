"""Shareable protected survey link ORM model."""

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, utc_now


class SurveyLink(Base):
    """Unguesseable public survey invitation link.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "survey_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    study: Mapped[str] = mapped_column(String, nullable=False)
    condition: Mapped[str | None] = mapped_column(String, nullable=True)
    label: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    response_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)
