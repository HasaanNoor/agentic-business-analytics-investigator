# Architecture Decision Records

Architecture Decision Records, or ADRs, document important architecture choices and the tradeoffs behind them. They are meant to explain why the system is shaped a certain way, not to replace implementation documentation or describe every file in detail.

Accepted ADRs describe the current architecture. They should be useful when reviewing the codebase, preparing for technical interviews, or deciding whether a future change is consistent with the existing design.

## Records

- [ADR 0001: Deterministic Analysis Before LLM Reasoning](0001-deterministic-analysis-before-llm-reasoning.md)
- [ADR 0002: Shared Data Provider Boundary for API and Static Modes](0002-shared-data-provider-boundary.md)
- [ADR 0003: Zero-Cost Static Portfolio Deployment](0003-zero-cost-static-portfolio-deployment.md)

Future decisions that replace or materially change an accepted ADR should create a new superseding ADR rather than silently rewriting history.
