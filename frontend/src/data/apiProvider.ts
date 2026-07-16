import {
  getActionableReport,
  getExplanations,
  getForecasts,
  getHealth,
  getIncident,
  getIncidents,
  getKpis,
  getLlmStatus,
  searchRag,
} from '../api/client';
import type { AnalyticsDataProvider } from './types';

export const apiDataProvider: AnalyticsDataProvider = {
  getHealth,
  getLlmStatus,
  getKpis,
  getIncidents,
  getIncident,
  getForecasts,
  getExplanations,
  getActionableReport,
  searchRag,
};
