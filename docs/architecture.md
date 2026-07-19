# Architecture

SentinelOps is a modular monolith for the MVP. FastAPI owns the API, SQLAlchemy stores domain and audit records, and an explicit transition graph prevents invalid or skipped stages. Provider output ends at typed Pydantic contracts. Evidence collection, patch inspection, command validation, verification, and approval are deterministic code.

The React client polls the persisted state and renders the same audit facts exposed by the API. The demo application writes JSON Lines to shared data directories and exposes Prometheus-compatible metrics. Codespaces runs the same Compose topology as local development and supports the nested restricted sandbox through Docker-in-Docker.

Every displayed explanation follows Observation → Evidence → Hypothesis → Test → Result → Decision. No hidden chain-of-thought is stored or displayed.
