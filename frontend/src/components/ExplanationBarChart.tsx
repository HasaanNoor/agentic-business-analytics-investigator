import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { ExplanationRow } from '../types/api';
import { formatNumber } from '../utils/format';

interface ExplanationBarChartProps {
  rows: ExplanationRow[];
}

export function ExplanationBarChart({ rows }: ExplanationBarChartProps) {
  const chartRows = rows
    .map((row) => ({
      feature: row.feature,
      value: row.mean_abs_attribution ?? row.importance ?? Math.abs(row.contribution ?? 0),
    }))
    .sort((a, b) => a.value - b.value);

  return (
    <div className="rounded border border-line bg-panel p-4 shadow-soft">
      <h2 className="text-base font-semibold text-ink">Ranked feature importance</h2>
      <div role="img" aria-label="Ranked SHAP feature importance chart" className="mt-4 h-96">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartRows} layout="vertical" margin={{ top: 8, right: 24, left: 80, bottom: 8 }}>
            <XAxis type="number" tick={{ fontSize: 12 }} />
            <YAxis type="category" dataKey="feature" width={150} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(value) => formatNumber(value)} />
            <Bar dataKey="value" fill="#246b73" radius={[0, 3, 3, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
