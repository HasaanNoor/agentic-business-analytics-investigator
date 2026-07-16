import type {
  ActionableReportResponse,
  ExplanationsResponse,
  ForecastsResponse,
  HealthResponse,
  Incident,
  IncidentsResponse,
  KpisResponse,
  LlmStatusResponse,
  RagSearchResponse,
} from '../types/api';
import type { DemoManifest } from './types';

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function hasCountedRows(value: unknown): value is { count: number; rows: unknown[] } {
  return isRecord(value) && typeof value.count === 'number' && Array.isArray(value.rows);
}

function assertValid<T>(value: unknown, valid: boolean, fixture: string): T {
  if (!valid) {
    throw new Error(`Static demo fixture "${fixture}" is invalid. Regenerate demo data and rebuild the frontend.`);
  }
  return value as T;
}

export function validateManifest(value: unknown): DemoManifest {
  const valid =
    isRecord(value) &&
    isString(value.schema_version) &&
    isString(value.generated_at) &&
    isString(value.dataset_name) &&
    isString(value.demonstration_label) &&
    isRecord(value.date_range) &&
    isString(value.date_range.start) &&
    isString(value.date_range.end);
  return assertValid<DemoManifest>(value, valid, 'manifest.json');
}

export function validateHealth(value: unknown): HealthResponse {
  const valid =
    isRecord(value) &&
    isString(value.status) &&
    isString(value.project) &&
    typeof value.read_only === 'boolean' &&
    isRecord(value.api) &&
    isRecord(value.database) &&
    isRecord(value.llm) &&
    isRecord(value.file_fallback) &&
    typeof value.ready === 'boolean';
  return assertValid<HealthResponse>(value, valid, 'health.json');
}

export function validateLlmStatus(value: unknown): LlmStatusResponse {
  const valid =
    isRecord(value) &&
    typeof value.enabled === 'boolean' &&
    typeof value.configured === 'boolean' &&
    isString(value.agent_mode) &&
    typeof value.fallback_enabled === 'boolean';
  return assertValid<LlmStatusResponse>(value, valid, 'llm_status.json');
}

export function validateKpis(value: unknown): KpisResponse {
  const valid = hasCountedRows(value) && value.rows.every((row) => isRecord(row) && isString(row.date));
  return assertValid<KpisResponse>(value, valid, 'kpis.json');
}

function isIncident(value: unknown): value is Incident {
  return isRecord(value) && isString(value.incident_id);
}

export function validateIncidents(value: unknown): IncidentsResponse {
  const valid = isRecord(value) && typeof value.count === 'number' && Array.isArray(value.incidents) && value.incidents.every(isIncident);
  return assertValid<IncidentsResponse>(value, valid, 'incidents.json');
}

export function validateForecasts(value: unknown): ForecastsResponse {
  const valid = hasCountedRows(value) && value.rows.every((row) => isRecord(row) && isString(row.date) && isString(row.kpi));
  return assertValid<ForecastsResponse>(value, valid, 'forecasts.json');
}

export function validateExplanations(value: unknown): ExplanationsResponse {
  const valid = hasCountedRows(value) && value.rows.every((row) => isRecord(row) && isString(row.kpi) && isString(row.feature));
  return assertValid<ExplanationsResponse>(value, valid, 'explanations.json');
}

export function validateActionableReport(value: unknown): ActionableReportResponse {
  const valid = isRecord(value) && isString(value.format) && isString(value.content);
  return assertValid<ActionableReportResponse>(value, valid, 'actionable_report.json');
}

export function validateRagSearch(value: unknown): RagSearchResponse {
  const valid = isRecord(value) && isString(value.query) && typeof value.count === 'number' && Array.isArray(value.results);
  return assertValid<RagSearchResponse>(value, valid, 'rag_search.json');
}
