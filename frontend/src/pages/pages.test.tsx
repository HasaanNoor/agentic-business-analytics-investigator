import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { App } from '../App';
import { dataProvider } from '../data/provider';
import { renderWithMemoryRouter } from '../test/render';
import { forecasts, health, incident, incidents, kpis, llmStatus } from '../test/testData';

vi.mock('../data/provider', () => {
  return {
    dataProvider: {
      getHealth: vi.fn(),
      getLlmStatus: vi.fn(),
      getKpis: vi.fn(),
      getIncidents: vi.fn(),
      getIncident: vi.fn(),
      getForecasts: vi.fn(),
      getExplanations: vi.fn().mockResolvedValue({ count: 1, rows: [{ kpi: 'net_revenue', feature: 'website_visitors', mean_abs_attribution: 10, rank: 1, model_name: 'linear_regression', explanation_method: 'SHAP LinearExplainer' }] }),
      getActionableReport: vi.fn().mockResolvedValue({ format: 'markdown', content: '# Report\n\nReview checkout.' }),
      searchRag: vi.fn(),
    },
  };
});

describe('dashboard pages', () => {
  beforeEach(() => {
    vi.mocked(dataProvider.getHealth).mockResolvedValue(health);
    vi.mocked(dataProvider.getLlmStatus).mockResolvedValue(llmStatus);
    vi.mocked(dataProvider.getKpis).mockResolvedValue(kpis);
    vi.mocked(dataProvider.getIncidents).mockResolvedValue(incidents);
    vi.mocked(dataProvider.getIncident).mockResolvedValue({ incident });
    vi.mocked(dataProvider.getForecasts).mockResolvedValue(forecasts);
    vi.mocked(dataProvider.searchRag).mockResolvedValue({
      query: 'checkout',
      count: 1,
      results: [{ similarity_score: 0.9, metadata: { incident_id: 'INC-099', root_cause: 'Deployment issue', resolution: 'Rollback', outcome: 'Recovered', recommendations: ['Rollback checkout change'], severity: 'high', region: 'All regions' } }],
    });
  });

  it('does not show the static demo notice in API mode', async () => {
    renderWithMemoryRouter(<App />, '/');
    expect(screen.queryByLabelText(/static portfolio demo notice/i)).not.toBeInTheDocument();
    expect(await screen.findByText('System readiness')).toBeInTheDocument();
  });

  it('shows loading and then renders overview data', async () => {
    renderWithMemoryRouter(<App />, '/');
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(await screen.findByText('System readiness')).toBeInTheDocument();
    expect(screen.getByText('Recent high-severity incidents')).toBeInTheDocument();
  });

  it('shows page error states with retry', async () => {
    vi.mocked(dataProvider.getKpis).mockRejectedValueOnce(new Error('The analytics API is currently unavailable. Confirm that the Docker stack or local FastAPI server is running.'));
    renderWithMemoryRouter(<App />, '/kpis');
    expect(await screen.findByRole('alert')).toHaveTextContent('analytics API is currently unavailable');
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });

  it('renders incident list rows', async () => {
    renderWithMemoryRouter(<App />, '/incidents');
    expect(await screen.findByRole('link', { name: 'INC-001' })).toBeInTheDocument();
    expect(screen.getByText('Likely platform reliability incident')).toBeInTheDocument();
  });

  it('renders incident detail findings', async () => {
    renderWithMemoryRouter(<App />, '/incidents/INC-001');
    expect(await screen.findByText(/Checkout Failure Spike Incident/)).toBeInTheDocument();
    expect(screen.getAllByText('Observations').length).toBeGreaterThan(0);
    expect(screen.getByText('Revenue Agent')).toBeInTheDocument();
    expect(screen.getByText('Provenance')).toBeInTheDocument();
  });

  it('submits RAG search explicitly', async () => {
    const user = userEvent.setup();
    renderWithMemoryRouter(<App />, '/rag');
    await user.type(screen.getByLabelText(/search query/i), 'checkout');
    await user.click(screen.getByRole('button', { name: /search/i }));
    await waitFor(() => expect(dataProvider.searchRag).toHaveBeenCalledWith('checkout', 3));
    expect(await screen.findByText('INC-099')).toBeInTheDocument();
  });

  it('displays LLM status without secrets', async () => {
    renderWithMemoryRouter(<App />, '/system');
    expect(await screen.findByText('LLM enabled')).toBeInTheDocument();
    expect(screen.queryByText('sk-test-secret')).not.toBeInTheDocument();
  });

  it('renders forecast and explanation pages', async () => {
    renderWithMemoryRouter(<App />, '/forecasts');
    expect(await screen.findByText(/seven-day planning forecasts/i)).toBeInTheDocument();
    expect(screen.getByText('Day 1')).toBeInTheDocument();
  });

  it('renders KPI chart summaries from returned rows', async () => {
    renderWithMemoryRouter(<App />, '/kpis');
    expect(await screen.findByText('Latest value')).toBeInTheDocument();
    const main = screen.getByRole('main');
    expect(within(main).getAllByText('$90').length).toBeGreaterThan(0);
  });
});
