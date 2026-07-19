# Architecture

SentinelOps is a modular monolith for the MVP. FastAPI owns the API, SQLAlchemy stores domain and audit records, and an explicit transition graph prevents invalid or skipped stages. Provider output ends at typed Pydantic contracts. Evidence collection, patch inspection, command validation, verification, and approval are deterministic code.

The React client auto-seeds a deterministic empty database, polls persisted state, and renders the same audit facts exposed by the API. Read-only `?demoState=` fixtures provide repeatable screenshots without changing persisted state. The demo application writes JSON Lines and exposes Prometheus-compatible metrics. Codespaces selects Docker when available and otherwise uses the restricted copied-workspace Local Sandbox.

Every displayed explanation follows Observation → Evidence → Hypothesis → Test → Result → Decision. No hidden chain-of-thought is stored or displayed.
