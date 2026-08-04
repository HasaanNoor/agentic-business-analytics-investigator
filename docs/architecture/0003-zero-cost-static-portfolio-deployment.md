# ADR 0003: Zero-Cost Static Portfolio Deployment

- Status: Accepted
- Date: 2026-08-04

## Context

The project has a full local architecture: FastAPI, React, PostgreSQL, Docker Compose, Alembic migrations, generated output files, database synchronization, deterministic analytics, optional OpenAI-powered reasoning, and file fallback behavior. It also has an AWS Terraform reference architecture for a future ECS/RDS/ALB deployment. The Terraform documentation is explicit that it defines infrastructure for review and validation, but does not apply Terraform, create cloud resources, build or push images, run AWS migrations, or run ECS services by default.

The public portfolio requirement is different. Reviewers should be able to open an interactive dashboard quickly without installing Docker, provisioning a database, configuring OpenAI credentials, or paying for cloud infrastructure. Expected traffic is low and intermittent, so keeping persistent AWS resources online would add cost and operational work without improving the main review experience.

The repository implements a GitHub Pages workflow that builds the frontend with `VITE_DATA_MODE=static` and uploads `frontend/dist` as the Pages artifact. The static demo uses pre-generated JSON fixtures exported from deterministic local outputs under `frontend/public/demo-data/`. It does not run FastAPI, connect to PostgreSQL, call OpenAI, perform live RAG retrieval, or create live investigations.

## Decision

Host the public interactive demonstration on GitHub Pages as a zero-cost static site. The static demo uses pre-generated outputs and performs no live backend computation.

Keep the full FastAPI/PostgreSQL/Docker application runnable locally. Keep the Terraform ECS/RDS/ALB architecture as a validated reference design in code and documentation. Do not claim that AWS infrastructure is currently deployed for the demo, and do not keep paid infrastructure running solely to support a low-traffic portfolio page.

## Alternatives considered

Leaving ECS, RDS, ALB, and NAT resources running continuously would demonstrate always-on cloud operations, but it would create ongoing cost for compute, database, load balancing, NAT, logging, and supporting resources. It would also require deployment credentials, image publishing, migrations, monitoring, and teardown discipline.

Deploying a lower-cost EC2 instance continuously would reduce some managed-service cost, but it would trade away the reference ECS/RDS architecture and still require server maintenance, patching, uptime management, database decisions, and secret handling. It would also be less representative of the Terraform design already documented.

Providing only source code with no public demo would avoid hosting work and cost entirely, but reviewers would need to clone, install, configure, and run the project before seeing the dashboard. That creates friction for a portfolio project where immediate access matters.

## Consequences

Positive consequences:

- The public demo has zero ongoing hosting cost through GitHub Pages.
- Reviewers get immediate access to the dashboard without local setup.
- The demo still exercises the real React pages, charts, components, routing, static provider, and fixture validation.
- Paid infrastructure is avoided unless there is a concrete need to operate the full stack.
- The production-oriented reference architecture remains preserved in Terraform and documentation.

Negative consequences:

- The public demo cannot run live investigations, live RAG retrieval, database writes, or OpenAI synthesis.
- There is no demonstration of always-on backend operations in the public URL.
- Static data can become stale if fixtures are not refreshed from deterministic outputs.
- Operational concerns such as migrations, ECS task rollout, RDS connectivity, and ALB routing remain documented and locally verifiable, but not visible in the hosted demo.

## When to revisit

Revisit this decision if the project starts receiving enough reviewer or user traffic to justify a live hosted backend, or if the portfolio goal changes from demonstrating the product surface to demonstrating always-on operations. Also revisit if a grant, employer account, or controlled evaluation environment removes the cost constraint and requires live investigation workflows, persistence, or authenticated user sessions.
