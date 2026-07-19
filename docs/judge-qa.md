# Judge Q&A

- **Is this just a coding assistant?** No. It owns a persisted incident lifecycle, gathers evidence, runs experiments, applies deterministic gates, and requests approval.
- **Why is it agentic?** It selects and executes bounded tools across observation, hypothesis, reproduction, repair and verification states.
- **Why is mock mode acceptable?** It makes judging deterministic and key-free while exercising the real state machine, tests, sandbox and policy.
- **What executes for real?** The failing API, telemetry, regression, copied workspace patch, tests, lint, type and security gates.
- **What is simulated?** The default PR is a local record and incidents 2–3 abstain after diagnosis.
- **How is unsafe code contained?** Network-disabled Docker or an allowlisted temporary Local Sandbox.
- **Why not auto-deploy?** Reliability changes require accountable human control and rollback ownership.
- **How do you prevent false fixes?** Reproduce first, require a failing regression before and passing regression after, then run mandatory gates.
- **Business value?** Lower triage time and toil without surrendering change control.
- **How would this scale?** Queue-backed workers, PostgreSQL, object telemetry stores, and ephemeral sandbox jobs.
- **Why one fully repairable incident?** The MVP prioritizes one credible end-to-end proof over shallow templates.
- **What data is required?** Scoped logs, metrics, traces, repository history and tests.
- **How are credentials protected?** Environment-only configuration, redacted provider errors, no sandbox secrets, and ignored `.env` files.
