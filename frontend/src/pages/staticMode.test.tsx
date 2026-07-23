import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { App } from '../App';
import { dataProvider } from '../data/provider';
import { renderWithMemoryRouter } from '../test/render';
import { forecasts, health, incident, incidents, kpis, llmStatus } from '../test/testData';

vi.mock('../config/dataMode', () => ({
  dataMode: 'static',
  isStaticDataMode: true,
  demoDataBaseUrl: '/demo-data/',
}));

vi.mock('../data/provider', () => ({
  dataProvider: {
    getHealth: vi.fn(),
    getLlmStatus: vi.fn(),
    getKpis: vi.fn(),
    getIncidents: vi.fn(),
    getIncident: vi.fn(),
    getForecasts: vi.fn(),
    getExplanations: vi.fn().mockResolvedValue({ count: 1, rows: [{ kpi: 'net_revenue', feature: 'website_visitors', mean_abs_attribution: 10, rank: 1 }] }),
    getActionableReport: vi.fn().mockResolvedValue({ format: 'markdown', content: '# Static report' }),
    searchRag: vi.fn(),
  },
}));

describe('static mode UI behavior', () => {
  beforeEach(() => {
    vi.mocked(dataProvider.getHealth).mockResolvedValue(health);
    vi.mocked(dataProvider.getLlmStatus).mockResolvedValue(llmStatus);
    vi.mocked(dataProvider.getKpis).mockResolvedValue(kpis);
    vi.mocked(dataProvider.getIncidents).mockResolvedValue(incidents);
    vi.mocked(dataProvider.getIncident).mockResolvedValue({ incident });
    vi.mocked(dataProvider.getForecasts).mockResolvedValue(forecasts);
    vi.mocked(dataProvider.searchRag).mockResolvedValue({
      query: 'checkout failures after deployment',
      count: 1,
      results: [{ similarity_score: 0.9, metadata: { incident_id: 'INC-099', root_cause: 'Deployment issue' } }],
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('shows a visible static demo notice', async () => {
    renderWithMemoryRouter(<App />, '/');
    expect(screen.getByLabelText(/static portfolio demo notice/i)).toHaveTextContent('Pre-generated sample dataset');
    expect(await screen.findByText('System readiness')).toBeInTheDocument();
  });

  it('shows compact portfolio-oriented overview status cards instead of unavailable infrastructure status', async () => {
    renderWithMemoryRouter(<App />, '/');

    expect(await screen.findByText('System readiness')).toBeInTheDocument();
    expect(screen.getByText('ready')).toBeInTheDocument();
    expect(screen.getByText('Portfolio demo ready for use.')).toBeInTheDocument();
    expect(screen.getByText('Deployment mode')).toBeInTheDocument();
    expect(screen.getByText('GitHub Pages')).toBeInTheDocument();
    expect(screen.getByText('Running from a versioned static demonstration dataset.')).toBeInTheDocument();
    expect(screen.getByText('Backend support')).toBeInTheDocument();
    expect(screen.getByText('supported')).toBeInTheDocument();
    expect(screen.getByText('The full backend is available through the local Docker deployment.')).toBeInTheDocument();
    expect(screen.getByText('Investigation mode')).toBeInTheDocument();
    expect(screen.getByText('deterministic')).toBeInTheDocument();
    expect(screen.getByText('Displaying stored investigation results.')).toBeInTheDocument();

    expect(screen.queryByText('Database availability')).not.toBeInTheDocument();
    expect(screen.queryByText('Database is not configured.')).not.toBeInTheDocument();
    expect(screen.queryByText('File fallback')).not.toBeInTheDocument();
    expect(screen.queryByText('GitHub Pages Demo')).not.toBeInTheDocument();
  });

  it('does not introduce FastAPI requests while rendering static mode', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch');

    renderWithMemoryRouter(<App />, '/');

    expect(await screen.findByText('System readiness')).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('uses a truthful replay action for historical search', async () => {
    const user = userEvent.setup();
    renderWithMemoryRouter(<App />, '/rag');
    expect(screen.getByLabelText(/search query/i)).toBeDisabled();
    expect(screen.getByText(/disables live retrieval controls/i)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /replay demo result/i }));
    await waitFor(() => expect(dataProvider.searchRag).toHaveBeenCalledWith('checkout failures after deployment', 3));
    expect(await screen.findByText('INC-099')).toBeInTheDocument();
  });
});
