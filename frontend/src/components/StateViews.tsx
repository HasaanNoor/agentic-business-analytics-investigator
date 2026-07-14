interface StateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function LoadingState({ message = 'Loading analytics data...' }: StateProps) {
  return (
    <div role="status" className="space-y-3 rounded border border-line bg-panel p-5 shadow-soft">
      <div className="h-4 w-56 animate-pulse rounded bg-slate-200" />
      <div className="h-24 animate-pulse rounded bg-slate-100" />
      <p className="text-sm text-muted">{message}</p>
    </div>
  );
}

export function ErrorState({ title = 'Could not load data', message, onRetry }: StateProps) {
  return (
    <div role="alert" className="rounded border border-red-200 bg-red-50 p-5 text-red-900">
      <h2 className="text-base font-semibold">{title}</h2>
      <p className="mt-2 text-sm">{message}</p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-4 rounded border border-red-300 bg-white px-3 py-2 text-sm font-medium text-red-800 hover:bg-red-100"
        >
          Retry
        </button>
      ) : null}
    </div>
  );
}

export function EmptyState({ title = 'No data available', message = 'No records matched the current view.' }: StateProps) {
  return (
    <div className="rounded border border-line bg-panel p-5 text-center shadow-soft">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      <p className="mt-2 text-sm text-muted">{message}</p>
    </div>
  );
}
