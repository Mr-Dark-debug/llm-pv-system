"""Benchmark prompt ORM model."""

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class Prompt(Base):
    """One standardized benchmark prompt.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prompt_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    prompt_type: Mapped[str] = mapped_column(String, nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    target_pv: Mapped[str | None] = mapped_column(String, nullable=True)
    expected_register: Mapped[str] = mapped_column(String, default="neutral")
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    responses: Mapped[list["LLMResponse"]] = relationship(back_populates="prompt", cascade="all, delete-orphan")
