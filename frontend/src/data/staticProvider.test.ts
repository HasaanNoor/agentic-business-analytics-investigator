import { afterEach, describe, expect, it, vi } from 'vitest';
import { clearStaticFixtureCache, staticDataProvider } from './staticProvider';
import { validateKpis } from './staticValidation';

function mockFixtureFetch(fixtures: Record<string, unknown>) {
  vi.stubGlobal(
    'fetch',
    vi.fn((url: string) => {
      const name = url.split('/').pop() || '';
      if (!(name in fixtures)) {
        return Promise.resolve({ ok: false, status: 404, headers: { get: () => 'application/json' }, json: () => Promise.resolve({}) });
      }
      return Promise.resolve({ ok: true, status: 200, headers: { get: () => 'application/json' }, json: () => Promise.resolve(fixtures[name]) });
    }),
  );
}

describe('static data provider', () => {
  afterEach(() => {
    clearStaticFixtureCache();
    vi.unstubAllGlobals();
  });

  it('loads and limits KPI fixtures', async () => {
    mockFixtureFetch({
      'kpis.json': {
        count: 2,
        rows: [
          { date: '2026-01-01', net_revenue: 100 },
          { date: '2026-01-02', net_revenue: 120 },
        ],
      },
    });
    await expect(staticDataProvider.getKpis(1)).resolves.toEqual({ count: 1, rows: [{ date: '2026-01-02', net_revenue: 120 }] });
  });

  it('fails clearly when a fixture is missing', async () => {
    mockFixtureFetch({});
    await expect(staticDataProvider.getForecasts()).rejects.toThrow('could not be loaded');
  });

  it('validates fixture shape before returning chart data', () => {
    expect(() => validateKpis({ count: 1, rows: [{ net_revenue: 100 }] })).toThrow('kpis.json');
  });
});
