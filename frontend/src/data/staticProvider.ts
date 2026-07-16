import { demoDataBaseUrl } from '../config/dataMode';
import { ApiError } from '../api/client';
import type { Incident } from '../types/api';
import type { AnalyticsDataProvider, DemoManifest } from './types';
import {
  validateActionableReport,
  validateExplanations,
  validateForecasts,
  validateHealth,
  validateIncidents,
  validateKpis,
  validateLlmStatus,
  validateManifest,
  validateRagSearch,
} from './staticValidation';

const cache = new Map<string, Promise<unknown>>();

async function loadJson(path: string): Promise<unknown> {
  const url = `${demoDataBaseUrl}${path}`;
  if (!cache.has(url)) {
    cache.set(
      url,
      fetch(url, { headers: { Accept: 'application/json' } }).then(async (response) => {
        if (!response.ok) {
          throw new ApiError(`Static demo fixture "${path}" could not be loaded. Rebuild the static demo fixtures.`, response.status);
        }
        try {
          return await response.json();
        } catch {
          throw new ApiError(`Static demo fixture "${path}" is not valid JSON.`);
        }
      }),
    );
  }
  return cache.get(url)!;
}

function applyLimit<T>(rows: T[], limit?: number): T[] {
  if (!limit) return rows;
  return rows.slice(Math.max(rows.length - limit, 0));
}

export function clearStaticFixtureCache() {
  cache.clear();
}

export const staticDataProvider: AnalyticsDataProvider = {
  async getDemoManifest(): Promise<DemoManifest> {
    return validateManifest(await loadJson('manifest.json'));
  },
  async getHealth() {
    return validateHealth(await loadJson('health.json'));
  },
  async getLlmStatus() {
    return validateLlmStatus(await loadJson('llm_status.json'));
  },
  async getKpis(limit?: number) {
    const response = validateKpis(await loadJson('kpis.json'));
    const rows = applyLimit(response.rows, limit);
    return { count: rows.length, rows };
  },
  async getIncidents() {
    return validateIncidents(await loadJson('incidents.json'));
  },
  async getIncident(id: string) {
    const response = validateIncidents(await loadJson('incidents.json'));
    const incident = response.incidents.find((item: Incident) => item.incident_id === id);
    if (!incident) throw new ApiError(`Static demo incident not found: ${id}`, 404);
    return { incident };
  },
  async getForecasts() {
    return validateForecasts(await loadJson('forecasts.json'));
  },
  async getExplanations(limit?: number) {
    const response = validateExplanations(await loadJson('explanations.json'));
    const rows = limit ? response.rows.slice(0, limit) : response.rows;
    return { count: rows.length, rows };
  },
  async getActionableReport() {
    return validateActionableReport(await loadJson('actionable_report.json'));
  },
  async searchRag() {
    return validateRagSearch(await loadJson('rag_search.json'));
  },
};
