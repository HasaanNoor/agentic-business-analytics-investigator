import type { AgentFinding } from '../types/api';
import { formatLabel, formatNumber } from '../utils/format';
import { StatusBadge } from './StatusBadge';

interface AgentFindingPanelProps {
  finding: AgentFinding;
}

export function AgentFindingPanel({ finding }: AgentFindingPanelProps) {
  return (
    <section className="rounded border border-line bg-panel p-4 shadow-soft">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-base font-semibold text-ink">{finding.agent || 'Agent finding'}</h3>
        <div className="flex gap-2">
          {finding.finding_type ? <StatusBadge value={formatLabel(finding.finding_type)} /> : null}
          {finding.confidence ? <StatusBadge value={`Confidence: ${finding.confidence}`} /> : null}
        </div>
      </div>
      {finding.summary ? <p className="mt-3 text-sm leading-6 text-muted">{finding.summary}</p> : null}
      {finding.supporting_evidence?.length ? (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-ink">Observations</h4>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
            {finding.supporting_evidence.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : null}
      {finding.recommended_next_steps?.length ? (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-ink">Recommendations</h4>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
            {finding.recommended_next_steps.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : null}
      {finding.metrics?.length ? (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-xs uppercase text-muted">
              <tr>
                <th className="border-b border-line py-2 pr-4">Metric</th>
                <th className="border-b border-line py-2 pr-4">Incident avg</th>
                <th className="border-b border-line py-2 pr-4">Baseline avg</th>
                <th className="border-b border-line py-2 pr-4">Change</th>
              </tr>
            </thead>
            <tbody>
              {finding.metrics.slice(0, 6).map((metric) => (
                <tr key={String(metric.metric)}>
                  <td className="border-b border-line py-2 pr-4 font-medium text-ink">{formatLabel(metric.metric)}</td>
                  <td className="border-b border-line py-2 pr-4 text-muted">{formatNumber(metric.incident_average)}</td>
                  <td className="border-b border-line py-2 pr-4 text-muted">{formatNumber(metric.baseline_average)}</td>
                  <td className="border-b border-line py-2 pr-4 text-muted">{formatNumber(metric.percent_change)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
