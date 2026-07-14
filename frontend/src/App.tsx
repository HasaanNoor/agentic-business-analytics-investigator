import { Navigate, Route, Routes } from 'react-router-dom';
import { AppShell } from './layouts/AppShell';
import { ExplainabilityPage } from './pages/ExplainabilityPage';
import { ForecastsPage } from './pages/ForecastsPage';
import { IncidentDetailPage } from './pages/IncidentDetailPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { KpisPage } from './pages/KpisPage';
import { OverviewPage } from './pages/OverviewPage';
import { RagPage } from './pages/RagPage';
import { ReportsPage } from './pages/ReportsPage';
import { SystemStatusPage } from './pages/SystemStatusPage';

export function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<OverviewPage />} />
        <Route path="kpis" element={<KpisPage />} />
        <Route path="incidents" element={<IncidentsPage />} />
        <Route path="incidents/:incidentId" element={<IncidentDetailPage />} />
        <Route path="forecasts" element={<ForecastsPage />} />
        <Route path="explanations" element={<ExplainabilityPage />} />
        <Route path="rag" element={<RagPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="system" element={<SystemStatusPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
