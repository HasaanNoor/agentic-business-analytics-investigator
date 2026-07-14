export type JsonRecord = Record<string, unknown>;

export interface HealthResponse {
  status: string;
  project: string;
  read_only: boolean;
  api: { status: string };
  database: {
    configured: boolean;
    available: boolean;
    error?: string | null;
  };
  llm: LlmStatusResponse;
  file_fallback: {
    available: boolean;
    missing_outputs: string[];
  };
  ready: boolean;
  files?: Record<string, { path: string; exists: boolean }>;
  missing_outputs?: string[];
}

export interface LlmStatusResponse {
  enabled: boolean;
  configured: boolean;
  selected_model: string | null;
  agent_mode: string;
  fallback_enabled: boolean;
  configuration_error?: string | null;
}

export interface KpiRow extends JsonRecord {
  date: string;
  net_revenue?: number;
  support_ticket_count?: number;
  shipping_delay_rate?: number;
  avg_api_latency_ms?: number;
  checkout_failure_rate?: number;
  warehouse_backlog?: number;
  carrier_capacity_utilization?: number;
  incident_signal?: boolean | number;
  dominant_incident_type?: string;
}

export interface KpisResponse {
  count: number;
  rows: KpiRow[];
}

export interface DateRange {
  start?: string | null;
  end?: string | null;
}

export interface AgentMetric extends JsonRecord {
  metric?: string;
  incident_average?: number;
  baseline_average?: number;
  change?: number;
  percent_change?: number;
  minimum?: number;
  maximum?: number;
}

export interface Provenance {
  execution_mode?: string | null;
  model_name?: string | null;
  generated_at?: string | null;
  fallback_used?: boolean | null;
  fallback_reason?: string | null;
  evidence_sources?: string[];
  prompt_version?: string | null;
  schema_version?: string | null;
}

export interface AgentFinding extends JsonRecord {
  agent?: string;
  finding_type?: string;
  summary?: string;
  supporting_evidence?: string[];
  recommended_next_steps?: string[];
  confidence?: string;
  metrics?: AgentMetric[];
  provenance?: Provenance;
}

export interface RetrievedIncident extends JsonRecord {
  incident_id?: string;
  incident_type?: string;
  similarity_score?: number;
  root_cause?: string;
  summary?: string;
  recommendations?: string[];
  metadata?: JsonRecord;
}

export interface Incident extends JsonRecord {
  incident_id: string;
  incident_title?: string;
  title?: string;
  date_range?: DateRange;
  incident_start_date?: string | null;
  incident_end_date?: string | null;
  main_anomaly_type?: string;
  related_anomaly_types?: string[];
  incident_severity?: string;
  severity?: string;
  affected_region?: string;
  region?: string;
  root_cause_category?: string;
  likely_cause?: string;
  business_impact_summary?: string;
  resolution_action?: string;
  resolution_success?: boolean;
  recovery_days?: number;
  affected_metrics?: string[];
  supporting_evidence?: string[];
  recommended_next_steps?: string[];
  recommendations?: string[];
  retrieved_incidents?: RetrievedIncident[];
  agent_findings?: AgentFinding[];
  execution_mode?: string | null;
  model_name?: string | null;
  fallback_used?: boolean | null;
  fallback_reason?: string | null;
  evidence_sources?: string[];
  prompt_version?: string | null;
  schema_version?: string | null;
  confidence_level?: string;
  limitations?: string[];
  provenance?: Provenance;
}

export interface IncidentsResponse {
  count: number;
  incidents: Incident[];
}

export interface IncidentResponse {
  incident: Incident;
}

export interface ForecastRow extends JsonRecord {
  date: string;
  kpi: string;
  forecast_day?: number;
  prediction?: number;
  forecast_value?: number;
  model_name?: string;
  selected_model?: string;
  rmse?: number;
  mae?: number;
  r2?: number;
}

export interface ForecastsResponse {
  count: number;
  rows: ForecastRow[];
}

export interface ExplanationRow extends JsonRecord {
  kpi: string;
  model_name?: string;
  feature: string;
  mean_abs_attribution?: number;
  importance?: number;
  contribution?: number;
  direction?: string;
  rank?: number;
  explanation_method?: string;
}

export interface ExplanationsResponse {
  count: number;
  rows: ExplanationRow[];
}

export interface ActionableReportResponse {
  format: string;
  content: string;
}

export interface RagResult extends JsonRecord {
  similarity_score?: number;
  metadata?: {
    incident_id?: string;
    incident_type?: string;
    summary?: string;
    root_cause?: string;
    resolution?: string;
    outcome?: string;
    recommendations?: string[];
    severity?: string;
    region?: string;
  } & JsonRecord;
}

export interface RagSearchResponse {
  query: string;
  count: number;
  results: RagResult[];
}
