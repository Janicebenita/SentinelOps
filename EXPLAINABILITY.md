# SentinelOps Reliability Engineer: Explainability

## Decision and reasoning

The agent's principal decision is which incident hypothesis is best supported and whether a bounded candidate patch is ready for human review. Its reasoning connects collected telemetry, Git evidence, source code, tests, and audit events to ranked, falsifiable hypotheses with explicit evidence for and against each explanation. A repair is not considered ready merely because a model recommends it: the original failure must be reproduced, the candidate must satisfy deterministic policy, and all required verification gates must pass.

## Inputs and data sources

Inputs include an incident description and the evidence available to the authorized workflow, such as structured logs, Prometheus metrics, traces, request identifiers, Git history, source files, tests, and persisted audit events. The agent also uses outputs from its isolated failure reproduction, generated regression test, candidate diff, and six verification gates covering regression, unit, integration, Ruff, MyPy, and Bandit. Every material workflow transition, artifact, command output, and approval event is recorded on the incident timeline.

## Limits and known constraints

The main limitation is that successful reproduction and verification within the available sandbox do not prove that a patch is safe in every production environment. SQLite is intended for a single demo or development instance, only the first seeded incident demonstrates the complete automated repair path, the local sandbox performs fewer checks than Docker mode, and the default pull-request artifact is simulated unless GitHub credentials are configured. Render deployments may cold-start and use ephemeral storage. SentinelOps never deploys automatically, and its candidate repair always remains subject to authorized human approval.
