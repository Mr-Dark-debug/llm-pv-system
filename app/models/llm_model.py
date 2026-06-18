"""LLM model registry ORM model."""

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class LLMModel(Base):
    """Benchmarked LLM metadata.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "llm_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    parameter_count_billion: Mapped[float | None] = mapped_column(Float, nullable=True)
    training_cutoff: Mapped[object | None] = mapped_column(Date, nullable=True)
    rlhf_tuned: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    pvr_overall: Mapped[float] = mapped_column(Float, default=0.0)
    n_literal_pv: Mapped[int] = mapped_column(Integer, default=0)
    n_semi_pv: Mapped[int] = mapped_column(Integer, default=0)
    n_figurative_pv: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    responses: Mapped[list["LLMResponse"]] = relationship(back_populates="model", cascade="all, delete-orphan")
