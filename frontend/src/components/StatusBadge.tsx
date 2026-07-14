interface StatusBadgeProps {
  value?: string | boolean | null;
  tone?: 'neutral' | 'success' | 'warning' | 'danger';
}

function inferTone(value?: string | boolean | null): StatusBadgeProps['tone'] {
  if (typeof value === 'boolean') return value ? 'success' : 'warning';
  const normalized = String(value || '').toLowerCase();
  if (['ready', 'ok', 'available', 'configured', 'enabled', 'success', 'false'].includes(normalized)) return 'success';
  if (['critical', 'high', 'degraded', 'unavailable', 'error', 'true'].includes(normalized)) return 'danger';
  if (['medium', 'fallback', 'deterministic', 'low'].includes(normalized)) return 'warning';
  return 'neutral';
}

export function StatusBadge({ value, tone }: StatusBadgeProps) {
  const actualTone: NonNullable<StatusBadgeProps['tone']> = tone || inferTone(value) || 'neutral';
  const classes = {
    neutral: 'border-slate-300 bg-slate-50 text-slate-700',
    success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
    warning: 'border-amber-200 bg-amber-50 text-amber-800',
    danger: 'border-red-200 bg-red-50 text-red-800',
  }[actualTone];

  return (
    <span className={`inline-flex items-center rounded border px-2 py-0.5 text-xs font-medium ${classes}`}>
      {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value || 'Unknown'}
    </span>
  );
}
