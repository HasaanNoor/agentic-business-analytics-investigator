# ADR 0002: Shared Data Provider Boundary for API and Static Modes

- Status: Accepted
- Date: 2026-08-04

## Context

The React dashboard must serve two different use cases. In the full local application, it reads live API responses from FastAPI, which can serve data from PostgreSQL or generated file fallback. In the portfolio demo, it runs as a static GitHub Pages site with no backend, no database, and no live investigation work.

The frontend still needs to present the same product surface in both modes: overview, KPI explorer, incident list and detail pages, forecasts, explainability, RAG search display, reports, health, and LLM status. The value of the demo depends on showing the real dashboard experience without maintaining a second UI.

The repository implements this through a data provider boundary. `frontend/src/data/types.ts` defines the provider contract. `apiProvider` delegates to the typed API client. `staticProvider` fetches JSON fixtures from `frontend/public/demo-data/`, validates them with static validation helpers, and returns API-shaped objects. `selectDataProvider` chooses between the two providers, and `frontend/src/config/dataMode.ts` reads `VITE_DATA_MODE`, defaulting to API mode unless the value is `static`.

Static mode also uses build-time configuration for the base path. The Pages workflow builds the frontend with `VITE_DATA_MODE=static` and `VITE_BASE_PATH=/agentic-business-analytics-investigator/`.

## Decision

Use one React frontend with interchangeable API and static data providers. The same pages, domain types, charts, components, formatters, and loading or error states are used in both modes. Only the data-access provider changes.

API mode reads from FastAPI through the existing frontend API client. Static mode reads versioned JSON fixtures under `frontend/public/demo-data/`. Selection occurs at the composition and configuration boundary through `VITE_DATA_MODE`, not inside every page component.

## Alternatives considered

Maintaining a separate static demo frontend would allow the demo to be optimized independently, but it would duplicate routes, components, charts, copy, and visual states. The demo could easily drift from the real application, especially as incident fields, report fields, and chart requirements change.

Embedding fixture-specific checks throughout components would avoid a formal provider boundary, but it would spread static-mode conditionals across the UI. Page code would need to know whether it is rendering API data or fixture data, which would make components harder to reason about and test.

Hosting the full backend only and having no static mode would keep one execution path for data access. It would also require always-on compute, database availability, and operational maintenance before a reviewer could try the dashboard. That is not aligned with a low-traffic portfolio project.

## Consequences

Positive consequences:

- UI duplication is avoided because API and static modes share the same presentation layer.
- Demo drift is reduced because changes to pages and components affect both modes.
- Static fixtures can be validated against expected frontend shapes before rendering.
- The public demo can be deployed without FastAPI, PostgreSQL, Docker, OpenAI, or AWS.
- Interview discussion can focus on a clean boundary: domain-facing provider interface on one side, environment-specific data access on the other.

Negative consequences:

- The provider interface must remain aligned with frontend needs as pages evolve.
- Static fixtures require schema discipline and periodic regeneration from deterministic outputs.
- Static mode can only replay stored data, so components that imply live computation must be labeled and handled carefully.
- Some API behavior, such as dynamic RAG query execution, must be represented by an API-shaped fixture rather than actual backend work.

## When to revisit

Revisit this decision if the frontend needs mode-specific workflows that cannot be represented behind the current provider contract. Also revisit if the static demo begins to require real persistence, authentication, live computation, or user-generated investigations. In that case, the project may need a hosted backend demo or a clearer split between public demo and full application experiences.
