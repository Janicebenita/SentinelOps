# Safety model

- Generated commands are parsed as argument arrays, restricted to an allowlist, and reject shell metacharacters.
- Sandbox containers run unprivileged, network-disabled, read-only, with CPU, memory, process, and time limits; no Docker socket or host secrets are mounted.
- `.env`, CI, policy, sandbox, deployment, secret, and migration paths are protected.
- Patches may touch at most five files and 150 changed lines, must add a regression test, and may not delete assertions, skip tests, disable checks, add credentials, or add network calls.
- The approval gate requires the original reproduction, before/after regression evidence, unit and integration tests, Ruff, MyPy, Bandit, policy compliance, and rollback plan.
- Human approval permits branch/commit/PR preparation only. No path deploys to production.
- Invalid or twice-malformed model responses are escalated.
# Finale safety invariants

- Every candidate references the same immutable twin manifest and seed.
- Candidate evaluation never writes to the original source tree.
- Docker uses `--network=none`, CPU/memory/process limits, a read-only base filesystem, a temporary writable workspace, and timeouts.
- Local fallback uses copied temporary workspaces, `shell=False`, exact predefined commands, and is labeled reduced assurance.
- Generated package installation and arbitrary shell commands are forbidden.
- Protected paths, assertions, tests, CI, security policy, and secrets cannot be silently modified.
- A failed mandatory gate makes a candidate ineligible regardless of its numerical score.
- Model confidence cannot override a deterministic failure.
- The red-team stage critiques candidates but cannot generate or approve a replacement.
- Approval remains human-only. No automatic deployment path exists.
- Audit chaining is tamper-evident integrity evidence, not blockchain, legal non-repudiation, or formal verification.

Blast radius and causal conclusions are estimates. The UI exposes assumptions, contradicting evidence, missing evidence, falsification tests, and confidence labels rather than presenting certainty.
