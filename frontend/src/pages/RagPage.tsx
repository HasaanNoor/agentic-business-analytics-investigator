import { FormEvent, useState } from 'react';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { StatusBadge } from '../components/StatusBadge';
import { isStaticDataMode } from '../config/dataMode';
import { dataProvider } from '../data/provider';
import type { RagSearchResponse } from '../types/api';
import { formatNumber } from '../utils/format';

const staticReplayQuery = 'checkout failures after deployment';

export function RagPage() {
  const [query, setQuery] = useState(isStaticDataMode ? staticReplayQuery : '');
  const [topK, setTopK] = useState(3);
  const [data, setData] = useState<RagSearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      setData(await dataProvider.searchRag(query.trim(), topK));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Historical Incident Search"
        description={
          isStaticDataMode
            ? 'Replay a stored historical-search result from the static demo fixtures. No embedding model or FastAPI endpoint runs in this mode.'
            : 'Submit an explicit query to retrieve similar historical incidents through the FastAPI RAG endpoint.'
        }
      />
      <form onSubmit={submit} className="grid gap-4 rounded border border-line bg-panel p-4 shadow-soft md:grid-cols-[1fr_160px_auto] md:items-end">
        <label className="text-sm font-medium text-ink">
          Search query
          <input
            className="mt-1 w-full rounded border border-line px-3 py-2 disabled:bg-slate-100 disabled:text-slate-600"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="checkout failures after deployment"
            disabled={isStaticDataMode}
            aria-describedby={isStaticDataMode ? 'static-rag-replay-note' : undefined}
          />
        </label>
        <label className="text-sm font-medium text-ink">
          Top K
          <select className="mt-1 w-full rounded border border-line px-3 py-2 disabled:bg-slate-100 disabled:text-slate-600" value={topK} onChange={(event) => setTopK(Number(event.target.value))} disabled={isStaticDataMode}>
            {[1, 2, 3, 5, 10].map((value) => <option key={value} value={value}>{value}</option>)}
          </select>
        </label>
        <button type="submit" className="rounded bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-[#1d5960]">
          {isStaticDataMode ? 'Replay demo result' : 'Search'}
        </button>
      </form>
      {isStaticDataMode ? (
        <p id="static-rag-replay-note" className="text-sm text-muted">
          Static mode disables live retrieval controls and replays one stored deterministic search result.
        </p>
      ) : null}
      {loading ? <LoadingState message="Searching historical incidents..." /> : null}
      {error ? <ErrorState message={error} /> : null}
      {!loading && !error && data ? (
        data.results.length ? (
          <div className="grid gap-4">
            {data.results.map((result, index) => {
              const metadata = result.metadata || {};
              return (
                <section key={`${metadata.incident_id}-${index}`} className="rounded border border-line bg-panel p-4 shadow-soft">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h2 className="text-base font-semibold text-ink">{metadata.incident_id || 'Historical incident'}</h2>
                    <div className="flex gap-2"><StatusBadge value={metadata.severity} /><StatusBadge value={metadata.region} /></div>
                  </div>
                  <p className="mt-2 text-sm text-muted">Similarity score: {formatNumber(result.similarity_score)}</p>
                  <dl className="mt-3 grid gap-3 text-sm md:grid-cols-2">
                    <div><dt className="font-medium text-ink">Summary</dt><dd className="text-muted">{metadata.summary || 'Not returned'}</dd></div>
                    <div><dt className="font-medium text-ink">Root cause</dt><dd className="text-muted">{metadata.root_cause || 'Not returned'}</dd></div>
                    <div><dt className="font-medium text-ink">Resolution</dt><dd className="text-muted">{metadata.resolution || 'Not returned'}</dd></div>
                    <div><dt className="font-medium text-ink">Outcome</dt><dd className="text-muted">{metadata.outcome || 'Not returned'}</dd></div>
                  </dl>
                  {metadata.recommendations?.length ? <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-muted">{metadata.recommendations.map((item) => <li key={item}>{item}</li>)}</ul> : null}
                </section>
              );
            })}
          </div>
        ) : <EmptyState title="No similar incidents found" />
      ) : null}
    </div>
  );
}
