import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { ForecastRow } from '../types/api';
import { formatKpiValue, getForecastValue, kpiLabels } from '../utils/format';

interface ForecastChartProps {
  rows: ForecastRow[];
  kpi: string;
}

export function ForecastChart({ rows, kpi }: ForecastChartProps) {
  const chartRows = rows
    .filter((row) => row.kpi === kpi && typeof getForecastValue(row) === 'number')
    .map((row) => ({ date: row.date, value: getForecastValue(row), forecast_day: row.forecast_day }));

  return (
    <div className="rounded border border-line bg-panel p-4 shadow-soft">
      <h2 className="text-base font-semibold text-ink">{kpiLabels[kpi] || kpi} seven-day forecast</h2>
      <p className="mt-1 text-sm text-muted">Forecasts are model outputs for planning, not guarantees.</p>
      <div role="img" aria-label={`${kpiLabels[kpi] || kpi} seven-day forecast chart`} className="mt-4 h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartRows} margin={{ top: 12, right: 24, left: 8, bottom: 8 }}>
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} width={72} />
            <Tooltip formatter={(value) => formatKpiValue(kpi, value)} labelFormatter={(label) => `Forecast date: ${label}`} />
            <Line type="monotone" dataKey="value" stroke="#246b73" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
