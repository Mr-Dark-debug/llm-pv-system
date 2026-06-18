"""User ORM model for researcher/admin accounts."""

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, utc_now


class User(Base):
    """Admin or researcher account.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="researcher")
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)
