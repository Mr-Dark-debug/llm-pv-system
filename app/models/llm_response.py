"""Raw LLM benchmark output ORM model."""

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class LLMResponse(Base):
    """Stored output for one model/prompt/run.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "llm_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("llm_models.id", ondelete="CASCADE"), nullable=False)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False)
    run_id: Mapped[int] = mapped_column(Integer, nullable=False)
    seed: Mapped[int] = mapped_column(Integer, nullable=False)
    output_text: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    pv_count: Mapped[int] = mapped_column(Integer, default=0)
    pvr_per_1k: Mapped[float] = mapped_column(Float, default=0.0)
    generation_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    api_latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    api_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String, default="mock")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    model: Mapped["LLMModel"] = relationship(back_populates="responses")
    prompt: Mapped["Prompt"] = relationship(back_populates="responses")
    detections: Mapped[list["PVDetection"]] = relationship(back_populates="response", cascade="all, delete-orphan")
