import { getHealth, getLlmStatus } from '../api/client';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { StatusBadge } from '../components/StatusBadge';
import { useAsyncData } from '../hooks/useAsyncData';

export function SystemStatusPage() {
  const { data, error, loading, retry } = useAsyncData(async () => {
    const [health, llm] = await Promise.all([getHealth(), getLlmStatus()]);
    return { health, llm };
  });

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data) return <EmptyState />;

  return (
    <div className="space-y-6">
      <PageHeader title="System Status" description="Operational status from health and LLM status endpoints. Credential values are never displayed." />
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {[
          ['API status', data.health.api.status],
          ['Readiness', data.health.status],
          ['Database connectivity', data.health.database.available],
          ['File fallback availability', data.health.file_fallback.available],
          ['LLM enabled', data.llm.enabled],
          ['LLM configured', data.llm.configured],
          ['Selected model', data.llm.selected_model || 'None'],
          ['Agent mode', data.llm.agent_mode],
          ['Fallback enabled', data.llm.fallback_enabled],
        ].map(([label, value]) => (
          <div key={String(label)} className="rounded border border-line bg-panel p-4 shadow-soft">
            <h2 className="text-sm font-medium text-muted">{label}</h2>
            <div className="mt-2"><StatusBadge value={value as string | boolean} /></div>
          </div>
        ))}
      </section>
      {data.llm.configuration_error ? (
        <section className="rounded border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
          <h2 className="font-semibold">LLM configuration issue</h2>
          <p className="mt-1">{data.llm.configuration_error}</p>
        </section>
      ) : null}
      <section className="rounded border border-line bg-panel p-4 shadow-soft">
        <h2 className="text-base font-semibold text-ink">Output files</h2>
        <div className="mt-3 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-xs uppercase text-muted"><tr><th className="border-b border-line py-2 pr-4">Output</th><th className="border-b border-line py-2 pr-4">Exists</th><th className="border-b border-line py-2 pr-4">Path</th></tr></thead>
            <tbody>
              {Object.entries(data.health.files || {}).map(([name, info]) => (
                <tr key={name}><td className="border-b border-line py-2 pr-4 font-medium">{name}</td><td className="border-b border-line py-2 pr-4"><StatusBadge value={info.exists} /></td><td className="border-b border-line py-2 pr-4 text-muted">{info.path}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
