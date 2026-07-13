"""Create database tables for local development."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.database.models import Base
from src.database.session import create_database_engine


def create_tables(database_url: str | None = None) -> None:
    engine = create_database_engine(database_url)
    Base.metadata.create_all(bind=engine)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create database tables from SQLAlchemy metadata.")
    parser.add_argument("--database-url", default=None, help="Optional database URL. Defaults to DATABASE_URL or local SQLite.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_tables(args.database_url)
    print("Database tables are ready.")


if __name__ == "__main__":
    main()
