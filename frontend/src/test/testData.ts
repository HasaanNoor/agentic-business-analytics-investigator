import type { ForecastsResponse, HealthResponse, Incident, IncidentsResponse, KpisResponse, LlmStatusResponse } from '../types/api';

export const health: HealthResponse = {
  status: 'ready',
  project: 'Agentic Business Analytics Investigator',
  read_only: true,
  api: { status: 'ok' },
  database: { configured: true, available: true, error: null },
  llm: {
    enabled: false,
    configured: false,
    selected_model: null,
    agent_mode: 'deterministic',
    fallback_enabled: true,
    configuration_error: null,
  },
  file_fallback: { available: true, missing_outputs: [] },
  ready: true,
  files: { kpis: { path: '/outputs/kpis.csv', exists: true } },
  missing_outputs: [],
};

export const llmStatus: LlmStatusResponse = health.llm;

export const kpis: KpisResponse = {
  count: 3,
  rows: [
    { date: '2026-01-01', net_revenue: 100, support_ticket_count: 10, shipping_delay_rate: 0.1, avg_api_latency_ms: 200, checkout_failure_rate: 0.02, warehouse_backlog: 30, carrier_capacity_utilization: 0.7, incident_signal: 0 },
    { date: '2026-01-02', net_revenue: 120, support_ticket_count: 12, shipping_delay_rate: 0.12, avg_api_latency_ms: 210, checkout_failure_rate: 0.03, warehouse_backlog: 40, carrier_capacity_utilization: 0.75, incident_signal: 1, dominant_incident_type: 'checkout_failure_spike' },
    { date: '2026-01-03', net_revenue: 90, support_ticket_count: 16, shipping_delay_rate: 0.2, avg_api_latency_ms: 250, checkout_failure_rate: 0.04, warehouse_backlog: 55, carrier_capacity_utilization: 0.8, incident_signal: 0 },
  ],
};

export const incident: Incident = {
  incident_id: 'INC-001',
  incident_title: 'Checkout Failure Spike Incident',
  date_range: { start: '2026-01-02', end: '2026-01-03' },
  main_anomaly_type: 'checkout_failure_spike',
  related_anomaly_types: ['latency_spike'],
  incident_severity: 'critical',
  affected_region: 'All regions',
  likely_cause: 'Likely platform reliability incident',
  root_cause_category: 'platform reliability',
  execution_mode: 'deterministic',
  fallback_used: false,
  fallback_reason: null,
  model_name: null,
  business_impact_summary: 'Checkout failures reduced conversion.',
  affected_metrics: ['net_revenue', 'checkout_failure_rate'],
  supporting_evidence: ['Checkout failure rate increased.'],
  recommended_next_steps: ['Review checkout deployment.'],
  retrieved_incidents: [{ incident_id: 'INC-099', similarity_score: 0.91, root_cause: 'Deployment issue', summary: 'Past checkout issue.' }],
  agent_findings: [
    { agent: 'Revenue Agent', finding_type: 'revenue', summary: 'Revenue decreased.', supporting_evidence: ['Revenue dropped.'], recommended_next_steps: ['Track recovery.'], confidence: 'high', metrics: [{ metric: 'net_revenue', incident_average: 90, baseline_average: 120, percent_change: -25 }] },
    { agent: 'Customer Support Agent', summary: 'Tickets increased.', confidence: 'medium' },
    { agent: 'Logistics Agent', summary: 'No logistics issue.', confidence: 'low' },
    { agent: 'Platform Reliability Agent', summary: 'Latency increased.', confidence: 'high' },
    { agent: 'Coordinator Agent', summary: 'Coordinate rollback.', confidence: 'medium' },
  ],
  provenance: {
    execution_mode: 'deterministic',
    fallback_used: false,
    evidence_sources: ['KPI summary'],
    prompt_version: null,
  },
  confidence_level: 'medium',
};

export const incidents: IncidentsResponse = { count: 1, incidents: [incident] };

export const forecasts: ForecastsResponse = {
  count: 2,
  rows: [
    { date: '2026-01-04', kpi: 'net_revenue', forecast_day: 1, prediction: 130, model_name: 'linear_regression' },
    { date: '2026-01-05', kpi: 'net_revenue', forecast_day: 2, prediction: 135, model_name: 'linear_regression' },
  ],
};
