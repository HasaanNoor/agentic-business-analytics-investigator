import { Line, LineChart, ReferenceDot, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { KpiRow } from '../types/api';
import { formatKpiValue, kpiLabels, toChartRows } from '../utils/format';

interface KpiLineChartProps {
  rows: KpiRow[];
  kpi: string;
  height?: number;
}

export function KpiLineChart({ rows, kpi, height = 280 }: KpiLineChartProps) {
  const chartRows = toChartRows(rows, kpi);
  const incidentRows = chartRows.filter((row) => row.incident);

  return (
    <div className="rounded border border-line bg-panel p-4 shadow-soft">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h2 className="text-base font-semibold text-ink">{kpiLabels[kpi] || kpi}</h2>
        <span className="text-xs text-muted">Incident markers show backend incident signals when available.</span>
      </div>
      <div role="img" aria-label={`${kpiLabels[kpi] || kpi} trend chart`} style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartRows} margin={{ top: 12, right: 24, left: 8, bottom: 8 }}>
            <XAxis dataKey="date" tick={{ fontSize: 12 }} minTickGap={30} />
            <YAxis tick={{ fontSize: 12 }} width={72} />
            <Tooltip formatter={(value) => formatKpiValue(kpi, value)} labelFormatter={(label) => `Date: ${label}`} />
            <Line type="monotone" dataKey="value" stroke="#246b73" strokeWidth={2} dot={false} />
            {incidentRows.map((row) => (
              <ReferenceDot key={`${row.date}-${row.value}`} x={row.date} y={row.value} r={4} fill="#b42318" stroke="#ffffff" />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
