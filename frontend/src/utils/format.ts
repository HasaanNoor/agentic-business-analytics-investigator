import type { ForecastRow, Incident, KpiRow } from '../types/api';

export const kpiLabels: Record<string, string> = {
  net_revenue: 'Net revenue',
  support_ticket_count: 'Support tickets',
  shipping_delay_rate: 'Shipping delay rate',
  avg_api_latency_ms: 'API latency',
  checkout_failure_rate: 'Checkout failure rate',
  warehouse_backlog: 'Warehouse backlog',
  carrier_capacity_utilization: 'Carrier capacity',
};

export const primaryKpis = Object.keys(kpiLabels);

export function formatLabel(value?: string | null): string {
  if (!value) return 'Not provided';
  return value.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());
}

export function formatNumber(value: unknown, options: Intl.NumberFormatOptions = {}): string {
  if (typeof value !== 'number' || Number.isNaN(value)) return 'Not available';
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: 2, ...options }).format(value);
}

export function formatKpiValue(kpi: string, value: unknown): string {
  if (kpi === 'net_revenue') return formatNumber(value, { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  if (kpi.includes('rate') || kpi.includes('utilization')) return formatNumber(typeof value === 'number' ? value * 100 : value, { maximumFractionDigits: 2 }) + '%';
  if (kpi.includes('latency')) return `${formatNumber(value, { maximumFractionDigits: 0 })} ms`;
  return formatNumber(value, { maximumFractionDigits: 0 });
}

export function getIncidentTitle(incident: Incident): string {
  return incident.incident_title || incident.title || incident.incident_id;
}

export function getIncidentSeverity(incident: Incident): string {
  return incident.incident_severity || incident.severity || 'unknown';
}

export function getIncidentRegion(incident: Incident): string {
  return incident.affected_region || incident.region || 'Not provided';
}

export function getIncidentStart(incident: Incident): string {
  return incident.date_range?.start || incident.incident_start_date || '';
}

export function getIncidentEnd(incident: Incident): string {
  return incident.date_range?.end || incident.incident_end_date || '';
}

export function getExecutionMode(incident: Incident): string {
  return incident.execution_mode || incident.provenance?.execution_mode || 'unknown';
}

export function getFallbackUsed(incident: Incident): boolean | null {
  if (typeof incident.fallback_used === 'boolean') return incident.fallback_used;
  if (typeof incident.provenance?.fallback_used === 'boolean') return incident.provenance.fallback_used;
  return null;
}

export function getForecastValue(row: ForecastRow): number | undefined {
  return row.prediction ?? row.forecast_value;
}

export function toChartRows(rows: KpiRow[], kpi: string) {
  return rows
    .filter((row) => typeof row[kpi] === 'number')
    .map((row) => ({
      date: row.date,
      value: row[kpi] as number,
      incident: Boolean(row.incident_signal),
      incidentType: row.dominant_incident_type,
    }));
}

export function summarizeValues(values: number[]) {
  if (!values.length) return { latest: undefined, average: undefined, min: undefined, max: undefined };
  const latest = values[values.length - 1];
  const average = values.reduce((sum, value) => sum + value, 0) / values.length;
  return { latest, average, min: Math.min(...values), max: Math.max(...values) };
}

export function severityRank(value?: string): number {
  const normalized = (value || '').toLowerCase();
  if (normalized === 'critical') return 4;
  if (normalized === 'high') return 3;
  if (normalized === 'medium') return 2;
  if (normalized === 'low') return 1;
  return 0;
}
