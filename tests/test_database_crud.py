from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import crud, models


def make_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
    return Session()


def test_crud_upserts_and_reads_api_records():
    session = make_session()

    crud.upsert_daily_kpi(session, {"date": date(2026, 1, 1), "net_revenue": 100.0, "business_incident_flag": False})
    crud.upsert_daily_kpi(session, {"date": date(2026, 1, 1), "net_revenue": 125.0, "business_incident_flag": True})
    crud.upsert_incident(
        session,
        {
            "incident_id": "INC-001",
            "incident_title": "Checkout issue",
            "date_range": {"start": "2026-01-01", "end": "2026-01-02"},
            "main_anomaly_type": "checkout_failure_spike",
        },
    )
    crud.upsert_forecast(
        session,
        {
            "date": date(2026, 1, 3),
            "kpi": "net_revenue",
            "forecast_day": 1,
            "prediction": 130.0,
            "model_name": "linear_regression",
        },
    )
    crud.upsert_shap_explanation(
        session,
        {
            "kpi": "net_revenue",
            "model_name": "linear_regression",
            "feature": "website_visitors",
            "mean_abs_attribution": 42.0,
            "rank": 1,
            "explanation_method": "SHAP",
        },
    )
    crud.upsert_actionable_report(
        session,
        {"report_name": "executive_operations_report", "format": "markdown", "content": "# Report"},
    )
    session.commit()

    assert crud.count_records(session, models.DailyKPI) == 1
    assert crud.list_kpis(session)[0]["net_revenue"] == 125.0
    assert crud.list_incidents(session)[0]["incident_id"] == "INC-001"
    assert crud.get_incident(session, "INC-001")["incident_title"] == "Checkout issue"
    assert crud.list_forecasts(session)[0]["prediction"] == 130.0
    assert crud.list_shap_explanations(session)[0]["feature"] == "website_visitors"
    assert crud.get_actionable_report(session)["content"] == "# Report"


def test_crud_reports_created_vs_updated():
    session = make_session()

    _, created_first = crud.upsert_model_metric(
        session,
        {"kpi": "net_revenue", "model_name": "linear_regression", "mae": 1.0, "selected_model": True},
    )
    _, created_second = crud.upsert_model_metric(
        session,
        {"kpi": "net_revenue", "model_name": "linear_regression", "mae": 2.0, "selected_model": True},
    )
    session.commit()

    row = session.query(models.ModelMetric).one()
    assert created_first is True
    assert created_second is False
    assert row.mae == 2.0

