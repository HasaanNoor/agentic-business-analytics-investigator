import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { StatusBadge } from '../components/StatusBadge';
import { isStaticDataMode } from '../config/dataMode';
import { dataProvider } from '../data/provider';
import { useAsyncData } from '../hooks/useAsyncData';
import { formatLabel, getExecutionMode, getFallbackUsed, getIncidentEnd, getIncidentRegion, getIncidentSeverity, getIncidentStart, getIncidentTitle, severityRank } from '../utils/format';

type SortMode = 'date-desc' | 'date-asc' | 'severity-desc' | 'severity-asc';

export function IncidentsPage() {
  const [query, setQuery] = useState('');
  const [severity, setSeverity] = useState('all');
  const [region, setRegion] = useState('all');
  const [mode, setMode] = useState('all');
  const [sort, setSort] = useState<SortMode>('date-desc');
  const { data, error, loading, retry } = useAsyncData(dataProvider.getIncidents);

  const regions = useMemo(() => Array.from(new Set((data?.incidents || []).map(getIncidentRegion))).sort(), [data]);
  const modes = useMemo(() => Array.from(new Set((data?.incidents || []).map(getExecutionMode))).sort(), [data]);

  const filtered = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    return [...(data?.incidents || [])]
      .filter((incident) => {
        const matchesQuery =
          !normalizedQuery ||
          incident.incident_id.toLowerCase().includes(normalizedQuery) ||
          getIncidentTitle(incident).toLowerCase().includes(normalizedQuery) ||
          (incident.main_anomaly_type || '').toLowerCase().includes(normalizedQuery);
        return (
          matchesQuery &&
          (severity === 'all' || getIncidentSeverity(incident).toLowerCase() === severity) &&
          (region === 'all' || getIncidentRegion(incident) === region) &&
          (mode === 'all' || getExecutionMode(incident) === mode)
        );
      })
      .sort((a, b) => {
        if (sort === 'severity-desc') return severityRank(getIncidentSeverity(b)) - severityRank(getIncidentSeverity(a));
        if (sort === 'severity-asc') return severityRank(getIncidentSeverity(a)) - severityRank(getIncidentSeverity(b));
        const diff = getIncidentStart(a).localeCompare(getIncidentStart(b));
        return sort === 'date-asc' ? diff : -diff;
      });
  }, [data, mode, query, region, severity, sort]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data?.incidents.length) return <EmptyState title="No incidents returned" />;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Incidents"
        description={
          isStaticDataMode
            ? 'Search, filter, sort, and open incident details from the pre-generated static demo incident set.'
            : 'Search, filter, sort, and open incident details from the FastAPI incident endpoint.'
        }
      />
      <section className="grid gap-4 rounded border border-line bg-panel p-4 shadow-soft md:grid-cols-5">
        <label className="text-sm font-medium text-ink md:col-span-2">
          Search incident id or type
          <input className="mt-1 w-full rounded border border-line px-3 py-2" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="INC-001 or checkout" />
        </label>
        <label className="text-sm font-medium text-ink">
          Severity
          <select className="mt-1 w-full rounded border border-line px-3 py-2" value={severity} onChange={(event) => setSeverity(event.target.value)}>
            <option value="all">All severities</option>
            {['critical', 'high', 'medium', 'low'].map((item) => (
              <option key={item} value={item}>
                {formatLabel(item)}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm font-medium text-ink">
          Region
          <select className="mt-1 w-full rounded border border-line px-3 py-2" value={region} onChange={(event) => setRegion(event.target.value)}>
            <option value="all">All regions</option>
            {regions.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm font-medium text-ink">
          Execution mode
          <select className="mt-1 w-full rounded border border-line px-3 py-2" value={mode} onChange={(event) => setMode(event.target.value)}>
            <option value="all">All modes</option>
            {modes.map((item) => (
              <option key={item} value={item}>
                {formatLabel(item)}
              </option>
            ))}
          </select>
        </label>
      </section>
      <label className="block max-w-xs text-sm font-medium text-ink">
        Sort
        <select className="mt-1 w-full rounded border border-line px-3 py-2" value={sort} onChange={(event) => setSort(event.target.value as SortMode)}>
          <option value="date-desc">Date, newest first</option>
          <option value="date-asc">Date, oldest first</option>
          <option value="severity-desc">Severity, highest first</option>
          <option value="severity-asc">Severity, lowest first</option>
        </select>
      </label>
      {filtered.length ? (
        <div className="overflow-x-auto rounded border border-line bg-panel shadow-soft">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-muted">
              <tr>
                <th className="px-4 py-3">Incident</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Date range</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Region</th>
                <th className="px-4 py-3">Root cause</th>
                <th className="px-4 py-3">Mode</th>
                <th className="px-4 py-3">Fallback</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((incident) => (
                <tr key={incident.incident_id} className="border-t border-line">
                  <td className="px-4 py-3 font-medium">
                    <Link to={`/incidents/${incident.incident_id}`} className="text-accent hover:underline">
                      {incident.incident_id}
                    </Link>
                    <div className="text-xs font-normal text-muted">{getIncidentTitle(incident)}</div>
                  </td>
                  <td className="px-4 py-3 text-muted">{formatLabel(incident.main_anomaly_type)}</td>
                  <td className="px-4 py-3 text-muted">{getIncidentStart(incident)} to {getIncidentEnd(incident) || getIncidentStart(incident)}</td>
                  <td className="px-4 py-3"><StatusBadge value={getIncidentSeverity(incident)} /></td>
                  <td className="px-4 py-3 text-muted">{getIncidentRegion(incident)}</td>
                  <td className="px-4 py-3 text-muted">{incident.likely_cause || 'Not provided'}</td>
                  <td className="px-4 py-3"><StatusBadge value={getExecutionMode(incident)} /></td>
                  <td className="px-4 py-3"><StatusBadge value={getFallbackUsed(incident)} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <EmptyState title="No matching incidents" />
      )}
    </div>
  );
}
