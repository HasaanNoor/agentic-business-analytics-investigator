import { useMemo, useState } from 'react';
import { getIncidents, getKpis } from '../api/client';
import { KpiLineChart } from '../components/KpiLineChart';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { SummaryCard } from '../components/SummaryCard';
import { useAsyncData } from '../hooks/useAsyncData';
import type { IncidentsResponse, KpisResponse } from '../types/api';
import { formatKpiValue, getIncidentEnd, getIncidentStart, kpiLabels, primaryKpis, summarizeValues, toChartRows } from '../utils/format';

export function KpisPage() {
  const [selectedKpi, setSelectedKpi] = useState('net_revenue');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const { data, error, loading, retry } = useAsyncData<{ kpis: KpisResponse; incidents: IncidentsResponse }>(async () => {
    const [kpis, incidents] = await Promise.all([getKpis(500), getIncidents()]);
    return { kpis, incidents };
  });

  const filteredRows = useMemo(() => {
    const rows = data?.kpis.rows || [];
    return rows.filter((row) => (!startDate || row.date >= startDate) && (!endDate || row.date <= endDate));
  }, [data, startDate, endDate]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data?.kpis.rows.length) return <EmptyState title="No KPI data" />;

  const values = toChartRows(filteredRows, selectedKpi).map((row) => row.value);
  const summary = summarizeValues(values);
  const relevantIncidents = data.incidents.incidents.filter((incident) => {
    const start = getIncidentStart(incident);
    const end = getIncidentEnd(incident) || start;
    return (!startDate || end >= startDate) && (!endDate || start <= endDate) && incident.affected_metrics?.includes(selectedKpi);
  });

  return (
    <div className="space-y-6">
      <PageHeader title="KPIs" description="Explore backend-provided KPI history with date filters and incident context. Summary values here are display summaries over returned API rows." />
      <section className="grid gap-4 rounded border border-line bg-panel p-4 shadow-soft md:grid-cols-3">
        <label className="text-sm font-medium text-ink">
          KPI
          <select className="mt-1 w-full rounded border border-line px-3 py-2" value={selectedKpi} onChange={(event) => setSelectedKpi(event.target.value)}>
            {primaryKpis.map((kpi) => (
              <option key={kpi} value={kpi}>
                {kpiLabels[kpi]}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm font-medium text-ink">
          Start date
          <input className="mt-1 w-full rounded border border-line px-3 py-2" type="date" value={startDate} onChange={(event) => setStartDate(event.target.value)} />
        </label>
        <label className="text-sm font-medium text-ink">
          End date
          <input className="mt-1 w-full rounded border border-line px-3 py-2" type="date" value={endDate} onChange={(event) => setEndDate(event.target.value)} />
        </label>
      </section>
      <section className="grid gap-4 md:grid-cols-4">
        <SummaryCard title="Latest value" value={formatKpiValue(selectedKpi, summary.latest)} />
        <SummaryCard title="Average" value={formatKpiValue(selectedKpi, summary.average)} />
        <SummaryCard title="Minimum" value={formatKpiValue(selectedKpi, summary.min)} />
        <SummaryCard title="Maximum" value={formatKpiValue(selectedKpi, summary.max)} />
      </section>
      {filteredRows.length ? <KpiLineChart rows={filteredRows} kpi={selectedKpi} /> : <EmptyState title="No rows match the selected dates" />}
      <section className="rounded border border-line bg-panel p-4 shadow-soft">
        <h2 className="text-base font-semibold text-ink">Incident markers</h2>
        {relevantIncidents.length ? (
          <ul className="mt-3 grid gap-2 md:grid-cols-2">
            {relevantIncidents.slice(0, 8).map((incident) => (
              <li key={incident.incident_id} className="rounded border border-line p-3 text-sm">
                <span className="font-medium text-ink">{incident.incident_id}</span>
                <span className="ml-2 text-muted">
                  {getIncidentStart(incident)} to {getIncidentEnd(incident) || getIncidentStart(incident)}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-sm text-muted">No incidents for this KPI and date range.</p>
        )}
      </section>
    </div>
  );
}
