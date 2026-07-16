/* eslint-disable no-unused-vars */
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

export interface DemoManifest {
  schema_version: string;
  generated_at: string;
  dataset_name: string;
  demonstration_label: string;
  date_range: {
    start: string;
    end: string;
  };
  source_descriptions?: string[];
  execution_mode?: string;
}

export interface AnalyticsDataProvider {
  getDemoManifest?: () => Promise<DemoManifest>;
  getHealth: () => Promise<HealthResponse>;
  getLlmStatus: () => Promise<LlmStatusResponse>;
  getKpis(limit?: number): Promise<KpisResponse>;
  getIncidents: () => Promise<IncidentsResponse>;
  getIncident(id: string): Promise<IncidentResponse>;
  getForecasts: () => Promise<ForecastsResponse>;
  getExplanations(limit?: number): Promise<ExplanationsResponse>;
  getActionableReport: () => Promise<ActionableReportResponse>;
  searchRag(query: string, topK?: number): Promise<RagSearchResponse>;
}
