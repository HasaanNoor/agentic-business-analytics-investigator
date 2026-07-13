from datetime import date

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.database import models


def test_database_tables_can_be_created_with_sqlite():
    engine = create_engine("sqlite:///:memory:", future=True)

    models.Base.metadata.create_all(engine)

    table_names = set(inspect(engine).get_table_names())
    assert {
        "daily_kpis",
        "anomaly_events",
        "incidents",
        "forecasts",
        "model_metrics",
        "shap_explanations",
        "rag_records",
        "actionable_reports",
        "pipeline_runs",
    }.issubset(table_names)


def test_unique_constraints_prevent_duplicate_natural_keys():
    engine = create_engine("sqlite:///:memory:", future=True)
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)

    with Session() as session:
        first = models.AnomalyEvent(date=date(2026, 1, 1), anomaly_type="latency_spike", metric="api_latency")
        duplicate = models.AnomalyEvent(date=date(2026, 1, 1), anomaly_type="latency_spike", metric="api_latency")
        session.add(first)
        session.commit()
        session.add(duplicate)

        try:
            session.commit()
        except Exception:
            session.rollback()
            duplicate_blocked = True
        else:
            duplicate_blocked = False

    assert duplicate_blocked is True
