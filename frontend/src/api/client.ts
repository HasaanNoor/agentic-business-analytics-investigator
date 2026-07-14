import type {
  ActionableReportResponse,
  ExplanationsResponse,
  ForecastsResponse,
  HealthResponse,
  IncidentResponse,
  IncidentsResponse,
  KpisResponse,
  LlmStatusResponse,
  RagSearchResponse,
} from '../types/api';

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const defaultBaseUrl = 'http://localhost:8000';
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || defaultBaseUrl).replace(/\/$/, '');

function endpoint(path: string): string {
  return `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;
}

function userFacingError(status?: number, detail?: unknown): string {
  const detailText = typeof detail === 'string' ? detail : undefined;
  if (status === 404) return detailText || 'The requested analytics record was not found.';
  if (status === 503) return detailText || 'The analytics API is temporarily unavailable.';
  if (status && status >= 500) return 'The analytics API returned an unexpected server error.';
  if (status && status >= 400) return detailText || 'The analytics API could not complete the request.';
  return 'The analytics API is currently unavailable. Confirm that the Docker stack or local FastAPI server is running.';
}

async function request<T>(path: string): Promise<T> {
  try {
    const response = await fetch(endpoint(path), {
      headers: { Accept: 'application/json' },
    });
    const contentType = response.headers.get('content-type') || '';
    const body = contentType.includes('application/json') ? await response.json() : undefined;
    if (!response.ok) {
      throw new ApiError(userFacingError(response.status, body?.detail), response.status);
    }
    return body as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(userFacingError());
  }
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>('/health');
}

export function getLlmStatus(): Promise<LlmStatusResponse> {
  return request<LlmStatusResponse>('/llm/status');
}

export function getKpis(limit = 120): Promise<KpisResponse> {
  return request<KpisResponse>(`/kpis?limit=${encodeURIComponent(limit)}`);
}

export function getIncidents(): Promise<IncidentsResponse> {
  return request<IncidentsResponse>('/incidents');
}

export function getIncident(id: string): Promise<IncidentResponse> {
  return request<IncidentResponse>(`/incidents/${encodeURIComponent(id)}`);
}

export function getForecasts(): Promise<ForecastsResponse> {
  return request<ForecastsResponse>('/forecasts');
}

export function getExplanations(limit = 100): Promise<ExplanationsResponse> {
  return request<ExplanationsResponse>(`/explanations?limit=${encodeURIComponent(limit)}`);
}

export function getActionableReport(): Promise<ActionableReportResponse> {
  return request<ActionableReportResponse>('/reports/actionable');
}

export function searchRag(query: string, topK = 3): Promise<RagSearchResponse> {
  const params = new URLSearchParams({ query, top_k: String(topK) });
  return request<RagSearchResponse>(`/rag/search?${params.toString()}`);
}
