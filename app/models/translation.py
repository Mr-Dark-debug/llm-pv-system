"""Translation task response ORM model."""

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class TranslationResponse(Base):
    """One translation item response.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "translation_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[str] = mapped_column(String, nullable=False)
    translated_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    pv_used: Mapped[bool] = mapped_column(Boolean, default=False)
    meaning_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    annotator_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    participant: Mapped["Participant"] = relationship(back_populates="translation_responses")
