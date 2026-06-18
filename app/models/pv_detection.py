"""Phrasal-verb detection ORM model."""

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class PVDetection(Base):
    """One detected phrasal verb in an LLM response.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "pv_detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("llm_responses.id", ondelete="CASCADE"), nullable=False)
    pv_lemma: Mapped[str] = mapped_column(String, nullable=False)
    verb: Mapped[str] = mapped_column(String, nullable=False)
    particle: Mapped[str] = mapped_column(String, nullable=False)
    sentence_index: Mapped[int] = mapped_column(Integer, default=0)
    token_start: Mapped[int] = mapped_column(Integer, default=0)
    token_end: Mapped[int] = mapped_column(Integer, default=0)
    transparency: Mapped[str] = mapped_column(String, default="semi_transparent")
    in_phave_list: Mapped[bool] = mapped_column(Boolean, default=False)
    layer1_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    annotator1_confirmed: Mapped[bool] = mapped_column(Boolean, default=True)
    annotator2_confirmed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    final_confirmed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    response: Mapped["LLMResponse"] = relationship(back_populates="detections")
