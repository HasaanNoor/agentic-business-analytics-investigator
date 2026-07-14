import { Link, useParams } from 'react-router-dom';
import { getIncident } from '../api/client';
import { AgentFindingPanel } from '../components/AgentFindingPanel';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { StatusBadge } from '../components/StatusBadge';
import { useAsyncData } from '../hooks/useAsyncData';
import type { Incident } from '../types/api';
import { formatLabel, formatNumber, getExecutionMode, getFallbackUsed, getIncidentEnd, getIncidentRegion, getIncidentSeverity, getIncidentStart, getIncidentTitle } from '../utils/format';

function ListBlock({ title, items }: { title: string; items?: string[] }) {
  return (
    <section className="rounded border border-line bg-panel p-4 shadow-soft">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      {items?.length ? (
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm leading-6 text-muted">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="mt-2 text-sm text-muted">Not provided.</p>
      )}
    </section>
  );
}

function agentByName(incident: Incident, name: string) {
  return incident.agent_findings?.find((finding) => finding.agent?.toLowerCase().includes(name));
}

export function IncidentDetailPage() {
  const { incidentId = '' } = useParams();
  const { data, error, loading, retry } = useAsyncData(() => getIncident(incidentId), [incidentId]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data?.incident) return <EmptyState title="Incident not found" />;

  const incident = data.incident;
  const provenance = incident.provenance || {};
  const evidenceSources = incident.evidence_sources || provenance.evidence_sources;
  const namedFindings = ['revenue', 'support', 'logistics', 'platform', 'coordinator']
    .map((name) => agentByName(incident, name))
    .filter(Boolean);

  return (
    <div className="space-y-6">
      <PageHeader
        title={`${incident.incident_id}: ${getIncidentTitle(incident)}`}
        description={`${getIncidentStart(incident)} to ${getIncidentEnd(incident) || getIncidentStart(incident)}. ${incident.business_impact_summary || ''}`}
        actions={<Link to="/incidents" className="rounded border border-line px-3 py-2 text-sm font-medium text-accent hover:bg-slate-50">Back to incidents</Link>}
      />
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded border border-line bg-panel p-4 shadow-soft"><h2 className="text-sm font-medium text-muted">Severity</h2><div className="mt-2"><StatusBadge value={getIncidentSeverity(incident)} /></div></div>
        <div className="rounded border border-line bg-panel p-4 shadow-soft"><h2 className="text-sm font-medium text-muted">Region</h2><p className="mt-2 font-semibold">{getIncidentRegion(incident)}</p></div>
        <div className="rounded border border-line bg-panel p-4 shadow-soft"><h2 className="text-sm font-medium text-muted">Execution mode</h2><div className="mt-2"><StatusBadge value={getExecutionMode(incident)} /></div></div>
        <div className="rounded border border-line bg-panel p-4 shadow-soft"><h2 className="text-sm font-medium text-muted">Fallback used</h2><div className="mt-2"><StatusBadge value={getFallbackUsed(incident)} /></div></div>
      </section>
      <section className="grid gap-4 lg:grid-cols-2">
        <section className="rounded border border-line bg-panel p-4 shadow-soft">
          <h2 className="text-base font-semibold text-ink">Observations</h2>
          <dl className="mt-3 grid gap-3 text-sm">
            <div><dt className="font-medium text-ink">Affected metrics</dt><dd className="mt-1 text-muted">{incident.affected_metrics?.map(formatLabel).join(', ') || 'Not provided'}</dd></div>
            <div><dt className="font-medium text-ink">Anomaly types</dt><dd className="mt-1 text-muted">{[incident.main_anomaly_type, ...(incident.related_anomaly_types || [])].filter(Boolean).map(formatLabel).join(', ') || 'Not provided'}</dd></div>
            <div><dt className="font-medium text-ink">Supporting evidence</dt><dd className="mt-1 text-muted">{incident.supporting_evidence?.join(' ') || 'Not provided'}</dd></div>
          </dl>
        </section>
        <section className="rounded border border-line bg-panel p-4 shadow-soft">
          <h2 className="text-base font-semibold text-ink">Inferences</h2>
          <dl className="mt-3 grid gap-3 text-sm">
            <div><dt className="font-medium text-ink">Likely root cause</dt><dd className="mt-1 text-muted">{incident.likely_cause || 'Not provided'}</dd></div>
            <div><dt className="font-medium text-ink">Root cause category</dt><dd className="mt-1 text-muted">{formatLabel(incident.root_cause_category)}</dd></div>
            <div><dt className="font-medium text-ink">Confidence</dt><dd className="mt-1 text-muted">{incident.confidence_level || 'Not provided'}</dd></div>
          </dl>
        </section>
      </section>
      <section className="grid gap-4 lg:grid-cols-2">
        <ListBlock title="Recommendations" items={incident.recommended_next_steps || incident.recommendations} />
        <ListBlock title="Limitations" items={incident.limitations || ['Review recommendations against current operational context before action.']} />
      </section>
      <section className="rounded border border-line bg-panel p-4 shadow-soft">
        <h2 className="text-base font-semibold text-ink">Historical incidents retrieved</h2>
        {incident.retrieved_incidents?.length ? (
          <div className="mt-3 overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="text-xs uppercase text-muted"><tr><th className="border-b border-line py-2 pr-4">Incident</th><th className="border-b border-line py-2 pr-4">Similarity</th><th className="border-b border-line py-2 pr-4">Root cause</th><th className="border-b border-line py-2 pr-4">Summary</th></tr></thead>
              <tbody>
                {incident.retrieved_incidents.map((item, index) => (
                  <tr key={`${item.incident_id}-${index}`}>
                    <td className="border-b border-line py-2 pr-4 font-medium">{item.incident_id || item.metadata?.incident_id as string}</td>
                    <td className="border-b border-line py-2 pr-4 text-muted">{formatNumber(item.similarity_score)}</td>
                    <td className="border-b border-line py-2 pr-4 text-muted">{item.root_cause || 'Not provided'}</td>
                    <td className="border-b border-line py-2 pr-4 text-muted">{item.summary || 'Not provided'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <p className="mt-2 text-sm text-muted">No retrieved incidents were returned.</p>}
      </section>
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-ink">Agent findings</h2>
        {namedFindings.length ? namedFindings.map((finding) => finding ? <AgentFindingPanel key={finding.agent} finding={finding} /> : null) : <EmptyState title="No agent findings returned" />}
      </section>
      <section className="rounded border border-line bg-panel p-4 shadow-soft">
        <h2 className="text-base font-semibold text-ink">Provenance</h2>
        <dl className="mt-3 grid gap-3 text-sm md:grid-cols-2">
          <div><dt className="font-medium text-ink">Model name</dt><dd className="text-muted">{incident.model_name || provenance.model_name || 'None'}</dd></div>
          <div><dt className="font-medium text-ink">Fallback reason</dt><dd className="text-muted">{incident.fallback_reason || provenance.fallback_reason || 'None'}</dd></div>
          <div><dt className="font-medium text-ink">Evidence sources</dt><dd className="text-muted">{evidenceSources?.join(', ') || 'Not provided'}</dd></div>
          <div><dt className="font-medium text-ink">Prompt version</dt><dd className="text-muted">{incident.prompt_version || provenance.prompt_version || 'Not applicable'}</dd></div>
        </dl>
      </section>
    </div>
  );
}
