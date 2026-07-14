import type { ReactNode } from 'react';

interface SummaryCardProps {
  title: string;
  value: ReactNode;
  detail?: ReactNode;
}

export function SummaryCard({ title, value, detail }: SummaryCardProps) {
  return (
    <section className="rounded border border-line bg-panel p-4 shadow-soft">
      <h3 className="text-sm font-medium text-muted">{title}</h3>
      <div className="mt-2 text-2xl font-semibold text-ink">{value}</div>
      {detail ? <div className="mt-2 text-sm text-muted">{detail}</div> : null}
    </section>
  );
}
