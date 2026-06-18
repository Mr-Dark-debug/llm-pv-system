"""Cached statistical analysis ORM model."""

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, utc_now


class AnalysisCache(Base):
    """JSON-encoded cached analysis result.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "analysis_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cache_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    analysis_type: Mapped[str] = mapped_column(String, nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)
