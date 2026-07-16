import { afterEach, describe, expect, it, vi } from 'vitest';

describe('data provider selection', () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.resetModules();
  });

  it('selects the API-backed provider by default', async () => {
    const [{ selectDataProvider }, { apiDataProvider }] = await Promise.all([import('./provider'), import('./apiProvider')]);
    expect(selectDataProvider('api')).toBe(apiDataProvider);
  });

  it('selects the static provider when requested', async () => {
    const [{ selectDataProvider }, { staticDataProvider }] = await Promise.all([import('./provider'), import('./staticProvider')]);
    expect(selectDataProvider('static')).toBe(staticDataProvider);
  });

  it('reads VITE_DATA_MODE=static at the composition boundary', async () => {
    vi.stubEnv('VITE_DATA_MODE', 'static');
    vi.resetModules();
    const [{ dataProvider }, { staticDataProvider }] = await Promise.all([import('./provider'), import('./staticProvider')]);
    expect(dataProvider).toBe(staticDataProvider);
  });
});
