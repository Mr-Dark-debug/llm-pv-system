"""Participant ORM model for L2 English learners."""

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utc_now


class Participant(Base):
    """Anonymous participant record.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    participant_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    study: Mapped[str] = mapped_column(String, nullable=False)
    condition: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    l1_language: Mapped[str | None] = mapped_column(String, nullable=True)
    l1_family: Mapped[str | None] = mapped_column(String, nullable=True)
    other_languages: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    education: Mapped[str | None] = mapped_column(String, nullable=True)
    years_english: Mapped[float | None] = mapped_column(Float, nullable=True)
    cefr_self_rating: Mapped[str | None] = mapped_column(String, nullable=True)
    opt_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attention_checks_passed: Mapped[int] = mapped_column(Integer, default=0)
    duration_minutes: Mapped[float | None] = mapped_column(Float, nullable=True)
    submission_timestamp: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)
    consented_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), default=utc_now)

    survey_responses: Mapped[list["SurveyResponse"]] = relationship(back_populates="participant", cascade="all, delete-orphan")
    forced_choice_responses: Mapped[list["ForcedChoiceResponse"]] = relationship(back_populates="participant", cascade="all, delete-orphan")
    translation_responses: Mapped[list["TranslationResponse"]] = relationship(back_populates="participant", cascade="all, delete-orphan")
    acceptability_responses: Mapped[list["AcceptabilityResponse"]] = relationship(back_populates="participant", cascade="all, delete-orphan")
