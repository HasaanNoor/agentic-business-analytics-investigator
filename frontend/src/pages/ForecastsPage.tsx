import { useMemo, useState } from 'react';
import { getForecasts } from '../api/client';
import { ForecastChart } from '../components/ForecastChart';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { StatusBadge } from '../components/StatusBadge';
import { useAsyncData } from '../hooks/useAsyncData';
import { formatKpiValue, getForecastValue, kpiLabels } from '../utils/format';

export function ForecastsPage() {
  const { data, error, loading, retry } = useAsyncData(getForecasts);
  const kpis = useMemo(() => Array.from(new Set((data?.rows || []).map((row) => row.kpi))), [data]);
  const [selectedKpi, setSelectedKpi] = useState('');
  const activeKpi = selectedKpi || kpis[0] || '';
  const rows = (data?.rows || []).filter((row) => row.kpi === activeKpi);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data?.rows.length) return <EmptyState title="No forecast data" />;

  return (
    <div className="space-y-6">
      <PageHeader title="Forecasts" description="Seven-day planning forecasts returned by FastAPI. These are model estimates, not guarantees." />
      <label className="block max-w-sm text-sm font-medium text-ink">
        KPI
        <select className="mt-1 w-full rounded border border-line px-3 py-2" value={activeKpi} onChange={(event) => setSelectedKpi(event.target.value)}>
          {kpis.map((kpi) => (
            <option key={kpi} value={kpi}>{kpiLabels[kpi] || kpi}</option>
          ))}
        </select>
      </label>
      <ForecastChart rows={data.rows} kpi={activeKpi} />
      <div className="overflow-x-auto rounded border border-line bg-panel shadow-soft">
        <table className="min-w-full text-left text-sm">
          <caption className="sr-only">Seven-day forecast table</caption>
          <thead className="bg-slate-50 text-xs uppercase text-muted">
            <tr><th className="px-4 py-3">KPI</th><th className="px-4 py-3">Forecast date</th><th className="px-4 py-3">Day</th><th className="px-4 py-3">Forecast value</th><th className="px-4 py-3">Model</th><th className="px-4 py-3">Metrics</th></tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={`${row.kpi}-${row.date}-${row.forecast_day}`} className="border-t border-line">
                <td className="px-4 py-3 font-medium">{kpiLabels[row.kpi] || row.kpi}</td>
                <td className="px-4 py-3 text-muted">{row.date}</td>
                <td className="px-4 py-3 text-muted">Day {row.forecast_day || 'N/A'}</td>
                <td className="px-4 py-3 text-muted">{formatKpiValue(row.kpi, getForecastValue(row))}</td>
                <td className="px-4 py-3"><StatusBadge value={row.model_name || row.selected_model} /></td>
                <td className="px-4 py-3 text-muted">{[row.rmse ? `RMSE ${row.rmse}` : '', row.mae ? `MAE ${row.mae}` : '', row.r2 ? `R2 ${row.r2}` : ''].filter(Boolean).join(', ') || 'Not returned'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
