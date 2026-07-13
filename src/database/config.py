"""Database configuration."""

from __future__ import annotations

import os


DEFAULT_DATABASE_URL = "sqlite:///./analytics_dev.db"


def get_database_url() -> str:
    """Return the configured database URL or a safe local default."""
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def is_database_configured() -> bool:
    """Return True when the application was explicitly configured to use a database."""
    return bool(os.getenv("DATABASE_URL"))
