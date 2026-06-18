"""FastAPI application factory."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import sessionmaker

from app.config import Settings, get_settings
from app.database import Base, create_engine_for_url, get_db, init_db
from app.routers import admin, analysis, benchmark, survey, views


def create_app(database_url: str | None = None) -> FastAPI:
    """Create and configure the FastAPI app.

    Args:
        database_url: Optional database URL override for tests.

    Returns:
        FastAPI: Configured application instance.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If startup database initialization fails.
    """

    settings = get_settings() if database_url is None else Settings(database_url=database_url)
    local_engine = create_engine_for_url(settings.database_url)
    local_session = sessionmaker(bind=local_engine, autocommit=False, autoflush=False)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
        """Initialize database during startup.

        Args:
            _app: FastAPI application instance.

        Returns:
            AsyncGenerator[None, None]: Lifespan context.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If database initialization fails.
        """

        Base.metadata.create_all(bind=local_engine)
        db = local_session()
        try:
            init_db(db)
        finally:
            db.close()
        yield

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    def _get_local_db():
        """Yield the app-local database session.

        Args:
            None.

        Returns:
            Generator[Session, None, None]: Database session generator.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If session handling fails.
        """

        db = local_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_local_db
    static_path = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    app.include_router(views.router)
    app.include_router(benchmark.router)
    app.include_router(survey.router)
    app.include_router(analysis.router)
    app.include_router(admin.router)

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        """Return a lightweight deployment health check.

        Args:
            None.

        Returns:
            dict[str, str]: Health status payload.

        Raises:
            None.
        """

        return {"status": "ok"}

    return app


app = create_app()
