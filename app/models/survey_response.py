"""Survey response ORM model for Studies 1 and 2."""

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class SurveyResponse(Base):
    """Full participant survey submission.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "survey_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id", ondelete="CASCADE"), nullable=False)
    study: Mapped[str] = mapped_column(String, nullable=False)
    llm_tools_used: Mapped[str | None] = mapped_column(Text, nullable=True)
    chatgpt_frequency: Mapped[int] = mapped_column(Integer, default=1)
    chatgpt_models: Mapped[str | None] = mapped_column(Text, nullable=True)
    claude_frequency: Mapped[int] = mapped_column(Integer, default=1)
    claude_models: Mapped[str | None] = mapped_column(Text, nullable=True)
    gemini_frequency: Mapped[int] = mapped_column(Integer, default=1)
    gemini_models: Mapped[str | None] = mapped_column(Text, nullable=True)
    copilot_frequency: Mapped[int] = mapped_column(Integer, default=1)
    deepl_frequency: Mapped[int] = mapped_column(Integer, default=1)
    perplexity_frequency: Mapped[int] = mapped_column(Integer, default=1)
    other_llm_frequency: Mapped[int] = mapped_column(Integer, default=1)
    other_llm_names: Mapped[str | None] = mapped_column(Text, nullable=True)
    daily_minutes_llm: Mapped[int] = mapped_column(Integer, default=0)
    duration_of_use_months: Mapped[int] = mapped_column(Integer, default=1)
    purpose_grammar: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose_vocab: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose_translation: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose_writing: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose_conversation: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose_reading: Mapped[bool] = mapped_column(Boolean, default=False)
    purpose_pronunciation: Mapped[bool] = mapped_column(Boolean, default=False)
    noticing_c7: Mapped[int | None] = mapped_column(Integer, nullable=True)
    noticing_c8: Mapped[bool] = mapped_column(Boolean, default=False)
    noticing_c10: Mapped[int | None] = mapped_column(Integer, nullable=True)
    noticing_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    qualitative_g1: Mapped[str | None] = mapped_column(Text, nullable=True)
    qualitative_g2: Mapped[str | None] = mapped_column(Text, nullable=True)
    lei: Mapped[float | None] = mapped_column(Float, nullable=True)
    pva: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    participant: Mapped["Participant"] = relationship(back_populates="survey_responses")
