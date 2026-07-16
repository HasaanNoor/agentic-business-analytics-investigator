import { Link } from 'react-router-dom';
import { KpiLineChart } from '../components/KpiLineChart';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { StatusBadge } from '../components/StatusBadge';
import { SummaryCard } from '../components/SummaryCard';
import { isStaticDataMode } from '../config/dataMode';
import { dataProvider } from '../data/provider';
import { useAsyncData } from '../hooks/useAsyncData';
import type { ForecastsResponse, HealthResponse, IncidentsResponse, KpisResponse } from '../types/api';
import { formatKpiValue, formatLabel, getIncidentSeverity, getIncidentTitle, kpiLabels, primaryKpis, severityRank } from '../utils/format';

interface OverviewData {
  health: HealthResponse;
  kpis: KpisResponse;
  incidents: IncidentsResponse;
  forecasts: ForecastsResponse;
}

export function OverviewPage() {
  const { data, error, loading, retry } = useAsyncData<OverviewData>(async () => {
    const [health, kpis, incidents, forecasts] = await Promise.all([dataProvider.getHealth(), dataProvider.getKpis(45), dataProvider.getIncidents(), dataProvider.getForecasts()]);
    return { health, kpis, incidents, forecasts };
  });

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data) return <EmptyState />;

  const latest = data.kpis.rows[data.kpis.rows.length - 1];
  const highSeverity = data.incidents.incidents
    .filter((incident) => severityRank(getIncidentSeverity(incident)) >= 3)
    .slice(-5)
    .reverse();
  const forecastKpis = Array.from(new Set(data.forecasts.rows.map((row) => row.kpi))).slice(0, 3);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Overview"
        description={
          isStaticDataMode
            ? 'Current operating status, latest KPI values, recent high-severity incidents, and forecast coverage from pre-generated static demo fixtures.'
            : 'Current operating status, latest KPI values, recent high-severity incidents, and forecast coverage from the FastAPI analytics service.'
        }
      />
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <SummaryCard title="System readiness" value={<StatusBadge value={data.health.status} />} detail={data.health.ready ? 'API reports ready for use.' : 'API reports degraded output availability.'} />
        <SummaryCard title="Database availability" value={<StatusBadge value={data.health.database.available} />} detail={data.health.database.configured ? 'PostgreSQL is configured.' : 'Database is not configured.'} />
        <SummaryCard title="File fallback" value={<StatusBadge value={data.health.file_fallback.available} />} detail={`${data.health.file_fallback.missing_outputs.length} missing output file(s).`} />
        <SummaryCard title="LLM mode" value={<StatusBadge value={data.health.llm.agent_mode} />} detail={data.health.llm.enabled ? data.health.llm.selected_model || 'Model not selected' : 'Deterministic mode available.'} />
      </section>

      {latest ? (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {primaryKpis.slice(0, 4).map((kpi) => (
            <SummaryCard key={kpi} title={kpiLabels[kpi]} value={formatKpiValue(kpi, latest[kpi])} detail={`Latest date: ${latest.date}`} />
          ))}
        </section>
      ) : (
        <EmptyState title="No KPI rows" />
      )}

      <section className="grid gap-4 xl:grid-cols-[2fr_1fr]">
        <KpiLineChart rows={data.kpis.rows} kpi="net_revenue" height={260} />
        <div className="rounded border border-line bg-panel p-4 shadow-soft">
          <h2 className="text-base font-semibold text-ink">Recent high-severity incidents</h2>
          {highSeverity.length ? (
            <ul className="mt-3 space-y-3">
              {highSeverity.map((incident) => (
                <li key={incident.incident_id} className="border-b border-line pb-3 last:border-0">
                  <Link to={`/incidents/${incident.incident_id}`} className="font-medium text-accent hover:underline">
                    {incident.incident_id}: {getIncidentTitle(incident)}
                  </Link>
                  <div className="mt-1 flex flex-wrap gap-2">
                    <StatusBadge value={getIncidentSeverity(incident)} />
                    <span className="text-xs text-muted">{formatLabel(incident.main_anomaly_type)}</span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-3 text-sm text-muted">No high-severity incidents returned.</p>
          )}
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded border border-line bg-panel p-4 shadow-soft">
          <h2 className="text-base font-semibold text-ink">Forecast summary</h2>
          <p className="mt-2 text-sm text-muted">Seven-day horizon available for {forecastKpis.map((kpi) => kpiLabels[kpi] || kpi).join(', ') || 'no KPIs'}.</p>
          <Link className="mt-4 inline-block text-sm font-medium text-accent hover:underline" to="/forecasts">
            Open forecasts
          </Link>
        </div>
        <div className="rounded border border-line bg-panel p-4 shadow-soft">
          <h2 className="text-base font-semibold text-ink">Quick links</h2>
          <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
            {[
              ['KPIs', '/kpis'],
              ['Incidents', '/incidents'],
              ['Explainability', '/explanations'],
              ['Historical Search', '/rag'],
            ].map(([label, href]) => (
              <Link key={href} to={href} className="rounded border border-line px-3 py-2 font-medium text-accent hover:bg-slate-50">
                {label}
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
