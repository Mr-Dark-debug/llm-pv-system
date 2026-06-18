"""SQLAlchemy engine, session, and database initialization helpers."""

from collections.abc import Generator
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp.

    Args:
        None.

    Returns:
        datetime: Current UTC timestamp.

    Raises:
        None.
    """

    return datetime.now(timezone.utc)


def create_engine_for_url(database_url: str | None = None) -> Engine:
    """Create a SQLite-aware SQLAlchemy engine.

    Args:
        database_url: Optional database URL override.

    Returns:
        Engine: Configured SQLAlchemy engine.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If engine creation fails.
    """

    url = database_url or get_settings().database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine_kwargs = {"connect_args": connect_args}
    if url == "sqlite://":
        engine_kwargs["poolclass"] = StaticPool
    if url.startswith("sqlite:///./"):
        Path(url.replace("sqlite:///./", "")).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url, **engine_kwargs)

    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
        """Enable SQLite foreign keys for cascading deletes.

        Args:
            dbapi_connection: Raw DB-API connection.
            _connection_record: SQLAlchemy connection record.

        Returns:
            None.

        Raises:
            Exception: If the PRAGMA cannot be executed.
        """

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


engine = create_engine_for_url()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for FastAPI dependency injection.

    Args:
        None.

    Returns:
        Generator[Session, None, None]: Request-scoped database session.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If session creation or closing fails.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(db: Session | None = None) -> None:
    """Create tables and seed protocol data.

    Args:
        db: Optional existing session; if omitted, a new session is created.

    Returns:
        None.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If schema creation or seeding fails.
    """

    from app.models import LLMModel, Prompt
    from app.seed_data import seed_models, seed_prompts

    bind = db.get_bind() if db is not None else engine
    Base.metadata.create_all(bind=bind)
    owns_session = db is None
    session = db or SessionLocal()
    try:
        existing_model_ids = {row[0] for row in session.query(LLMModel.model_id).all()}
        for model in seed_models():
            if model.model_id not in existing_model_ids:
                session.add(model)
        if session.query(Prompt).count() == 0:
            session.add_all(seed_prompts())
        session.commit()
    finally:
        if owns_session:
            session.close()
