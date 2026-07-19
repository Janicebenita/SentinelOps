# Safety model

- Generated commands are parsed as argument arrays, restricted to an allowlist, and reject shell metacharacters.
- Sandbox containers run unprivileged, network-disabled, read-only, with CPU, memory, process, and time limits; no Docker socket or host secrets are mounted.
- `.env`, CI, policy, sandbox, deployment, secret, and migration paths are protected.
- Patches may touch at most five files and 150 changed lines, must add a regression test, and may not delete assertions, skip tests, disable checks, add credentials, or add network calls.
- The approval gate requires the original reproduction, before/after regression evidence, unit and integration tests, Ruff, MyPy, Bandit, policy compliance, and rollback plan.
- Human approval permits branch/commit/PR preparation only. No path deploys to production.
- Invalid or twice-malformed model responses are escalated.
