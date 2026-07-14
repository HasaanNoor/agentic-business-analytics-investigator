import { afterEach, describe, expect, it, vi } from 'vitest';
import { getHealth, getKpis, searchRag } from './client';

function mockFetch(response: unknown, ok = true, status = 200) {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
    ok,
    status,
    headers: { get: () => 'application/json' },
    json: () => Promise.resolve(response),
  }));
}

describe('api client', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('loads typed API responses', async () => {
    mockFetch({ status: 'ready' });
    await expect(getHealth()).resolves.toEqual({ status: 'ready' });
  });

  it('handles non-200 responses with user-facing errors', async () => {
    mockFetch({ detail: 'Required output file is missing' }, false, 404);
    await expect(getKpis()).rejects.toThrow('Required output file is missing');
  });

  it('encodes RAG search parameters', async () => {
    mockFetch({ query: 'checkout failures', count: 0, results: [] });
    await searchRag('checkout failures', 5);
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('query=checkout+failures&top_k=5'), expect.any(Object));
  });
});
