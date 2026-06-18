"""Acceptability-judgement response ORM model."""

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class AcceptabilityResponse(Base):
    """One acceptability judgement rating.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "acceptability_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    pv_variant: Mapped[bool] = mapped_column(Boolean, default=True)
    response_timestamp: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    participant: Mapped["Participant"] = relationship(back_populates="acceptability_responses")
