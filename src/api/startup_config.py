"""Focused startup configuration validation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


TRUTHY = {"true", "1", "yes", "y", "on"}
FALSY = {"false", "0", "no", "n", "off"}
LOCAL_APP_ENVS = {"", "development", "dev", "local", "test"}
DEVELOPMENT_DATABASE_USERS = {"analytics_user"}
DEVELOPMENT_DATABASE_PASSWORDS = {"analytics_password"}
DEVELOPMENT_DATABASE_NAMES = {"analytics_local"}


class StartupConfigError(ValueError):
    """Raised when startup configuration is unsafe or invalid."""


@dataclass(frozen=True)
class StartupConfig:
    app_env: str
    production: bool
    run_migrations_on_startup: bool
    sync_outputs_on_startup: bool
    database_url_present: bool


def parse_bool(name: str, value: str | None, default: bool = False) -> bool:
    """Parse a strict boolean environment value."""
    if value is None or value == "":
        return default
    normalized = value.strip().lower()
    if normalized in TRUTHY:
        return True
    if normalized in FALSY:
        return False
    raise StartupConfigError(f"{name} must be true or false.")


def load_startup_config(env: Mapping[str, str] | None = None) -> StartupConfig:
    source = env if env is not None else os.environ
    app_env = source.get("APP_ENV", "development").strip().lower()
    return StartupConfig(
        app_env=app_env,
        production=app_env == "production",
        run_migrations_on_startup=parse_bool(
            "RUN_MIGRATIONS_ON_STARTUP",
            source.get("RUN_MIGRATIONS_ON_STARTUP"),
            default=False,
        ),
        sync_outputs_on_startup=parse_bool(
            "SYNC_OUTPUTS_ON_STARTUP",
            source.get("SYNC_OUTPUTS_ON_STARTUP"),
            default=False,
        ),
        database_url_present=bool(source.get("DATABASE_URL")),
    )


def validate_startup_config(env: Mapping[str, str] | None = None) -> StartupConfig:
    """Validate API startup settings and return the parsed configuration."""
    source = env if env is not None else os.environ
    config = load_startup_config(source)
    if config.production:
        errors: list[str] = []
        if config.run_migrations_on_startup:
            errors.append(
                "RUN_MIGRATIONS_ON_STARTUP must be false for production API replicas; "
                "run `migrate` as a separate deployment task."
            )
        if config.sync_outputs_on_startup:
            errors.append(
                "SYNC_OUTPUTS_ON_STARTUP must be false for production API replicas; "
                "run `sync` as a separate deployment task."
            )
        if not config.database_url_present:
            errors.append("DATABASE_URL is required when APP_ENV=production.")
        errors.extend(_production_database_errors(source.get("DATABASE_URL")))
        if errors:
            raise StartupConfigError("Invalid production startup configuration: " + " ".join(errors))
    elif config.app_env not in LOCAL_APP_ENVS:
        raise StartupConfigError("APP_ENV must be production, development, local, dev, or test.")
    return config


def _production_database_errors(database_url: str | None) -> list[str]:
    if not database_url:
        return []
    try:
        url = make_url(database_url)
    except ArgumentError:
        return ["DATABASE_URL is not a valid SQLAlchemy database URL."]
    errors: list[str] = []
    if url.drivername.startswith("sqlite"):
        errors.append("SQLite DATABASE_URL is not accepted when APP_ENV=production.")
    if url.username in DEVELOPMENT_DATABASE_USERS:
        errors.append("DATABASE_URL uses a default development database username.")
    if url.password in DEVELOPMENT_DATABASE_PASSWORDS:
        errors.append("DATABASE_URL uses a default development database password.")
    if url.database in DEVELOPMENT_DATABASE_NAMES:
        errors.append("DATABASE_URL uses a default development database name.")
    return errors


def main() -> None:
    validate_startup_config()


if __name__ == "__main__":
    main()
