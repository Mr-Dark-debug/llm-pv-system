"""Single-command entry point for the LEI/PVA FastAPI server."""

import os

import uvicorn

from app.config import get_settings
from app.database import init_db


def main() -> None:
    """Initialize the database and start Uvicorn.

    Args:
        None.

    Returns:
        None.

    Raises:
        Exception: If database initialization or server startup fails.
    """

    init_db()
    settings = get_settings()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=settings.debug)


if __name__ == "__main__":
    main()
