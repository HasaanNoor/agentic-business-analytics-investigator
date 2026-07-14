import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { getActionableReport } from '../api/client';
import { PageHeader } from '../components/PageHeader';
import { EmptyState, ErrorState, LoadingState } from '../components/StateViews';
import { useAsyncData } from '../hooks/useAsyncData';

export function ReportsPage() {
  const { data, error, loading, retry } = useAsyncData(getActionableReport);
  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={retry} />;
  if (!data?.content) return <EmptyState title="No actionable report content" />;

  return (
    <div className="space-y-6">
      <PageHeader title="Actionable Report" description="Markdown returned by the FastAPI report endpoint. Raw HTML is not enabled." />
      <article className="markdown-report rounded border border-line bg-panel p-5 shadow-soft">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{data.content}</ReactMarkdown>
      </article>
    </div>
  );
}
