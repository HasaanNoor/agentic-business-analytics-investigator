import { NavLink, Outlet } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Overview' },
  { to: '/kpis', label: 'KPIs' },
  { to: '/incidents', label: 'Incidents' },
  { to: '/forecasts', label: 'Forecasts' },
  { to: '/explanations', label: 'Explainability' },
  { to: '/rag', label: 'Historical Search' },
  { to: '/reports', label: 'Actionable Report' },
  { to: '/system', label: 'System Status' },
];

export function AppShell() {
  return (
    <div className="min-h-screen bg-canvas text-ink">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-panel p-5 lg:block">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-accent">Northstar Commerce</p>
          <p className="mt-2 text-lg font-semibold leading-6 text-ink">Agentic Analytics</p>
        </div>
        <nav aria-label="Primary navigation" className="mt-8 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `block rounded px-3 py-2 text-sm font-medium ${
                  isActive ? 'bg-accent text-white' : 'text-slate-700 hover:bg-slate-100 hover:text-ink'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-line bg-panel/95 px-4 py-3 backdrop-blur lg:hidden">
          <label htmlFor="mobile-nav" className="sr-only">
            Navigate to section
          </label>
          <select
            id="mobile-nav"
            aria-label="Primary navigation"
            className="w-full rounded border border-line bg-white px-3 py-2 text-sm"
            onChange={(event) => {
              window.location.href = event.target.value;
            }}
            defaultValue={window.location.pathname}
          >
            {navItems.map((item) => (
              <option key={item.to} value={item.to}>
                {item.label}
              </option>
            ))}
          </select>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6 md:px-6 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
