"""add llm investigation provenance

Revision ID: 20260713_1500
Revises: 20260712_1300
Create Date: 2026-07-13 15:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260713_1500"
down_revision = "20260712_1300"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("incidents", sa.Column("execution_mode", sa.String(length=50), nullable=True))
    op.add_column("incidents", sa.Column("model_name", sa.String(length=120), nullable=True))
    op.add_column("incidents", sa.Column("fallback_used", sa.Boolean(), nullable=True))
    op.add_column("incidents", sa.Column("fallback_reason", sa.Text(), nullable=True))
    op.add_column("incidents", sa.Column("provenance", sa.JSON(), nullable=True))
    op.add_column("incidents", sa.Column("prompt_version", sa.String(length=120), nullable=True))
    op.add_column("incidents", sa.Column("schema_version", sa.String(length=120), nullable=True))
    op.create_index("ix_incidents_execution_mode", "incidents", ["execution_mode"])
    op.create_index("ix_incidents_fallback_used", "incidents", ["fallback_used"])


def downgrade() -> None:
    op.drop_index("ix_incidents_fallback_used", table_name="incidents")
    op.drop_index("ix_incidents_execution_mode", table_name="incidents")
    op.drop_column("incidents", "schema_version")
    op.drop_column("incidents", "prompt_version")
    op.drop_column("incidents", "provenance")
    op.drop_column("incidents", "fallback_reason")
    op.drop_column("incidents", "fallback_used")
    op.drop_column("incidents", "model_name")
    op.drop_column("incidents", "execution_mode")

