import { useMemo, useState } from 'react';
import { getExplanations } from '../api/client';
import { ExplanationBarChart } from '../components/ExplanationBarChart';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { useAsyncData } from '../hooks/useAsyncData';
import { formatNumber, kpiLabels } from '../utils/format';

export function ExplainabilityPage() {
  const { data, error, loading, retry } = useAsyncData(() => getExplanations(500));
  const kpis = useMemo(() => Array.from(new Set((data?.rows || []).map((row) => row.kpi))), [data]);
  const [selectedKpi, setSelectedKpi] = useState('');
  const activeKpi = selectedKpi || kpis[0] || '';
  const rows = (data?.rows || []).filter((row) => row.kpi === activeKpi).sort((a, b) => (a.rank || 999) - (b.rank || 999));

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data?.rows.length) return <EmptyState title="No explanation data" />;

  return (
    <div className="space-y-6">
      <PageHeader title="Explainability" description="SHAP describes how the selected model used features. It explains model behavior and does not prove real-world causation." />
      <label className="block max-w-sm text-sm font-medium text-ink">
        KPI
        <select className="mt-1 w-full rounded border border-line px-3 py-2" value={activeKpi} onChange={(event) => setSelectedKpi(event.target.value)}>
          {kpis.map((kpi) => <option key={kpi} value={kpi}>{kpiLabels[kpi] || kpi}</option>)}
        </select>
      </label>
      <ExplanationBarChart rows={rows} />
      <div className="overflow-x-auto rounded border border-line bg-panel shadow-soft">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase text-muted"><tr><th className="px-4 py-3">Rank</th><th className="px-4 py-3">Feature</th><th className="px-4 py-3">Importance</th><th className="px-4 py-3">Direction</th><th className="px-4 py-3">Model</th><th className="px-4 py-3">Method</th></tr></thead>
          <tbody>
            {rows.map((row) => (
              <tr key={`${row.kpi}-${row.feature}`} className="border-t border-line">
                <td className="px-4 py-3">{row.rank || 'N/A'}</td>
                <td className="px-4 py-3 font-medium">{row.feature}</td>
                <td className="px-4 py-3 text-muted">{formatNumber(row.mean_abs_attribution ?? row.importance ?? row.contribution)}</td>
                <td className="px-4 py-3 text-muted">{row.direction || 'Not returned'}</td>
                <td className="px-4 py-3 text-muted">{row.model_name || 'Not returned'}</td>
                <td className="px-4 py-3 text-muted">{row.explanation_method || 'Not returned'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
