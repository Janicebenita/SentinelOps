# SentinelOps submission summary

**Problem:** incident responders correlate fragmented telemetry and code under time pressure, while unbounded coding agents risk false fixes. **Solution:** SentinelOps is an evidence-first autonomous reliability engineer for human-approved repair. **Users:** SRE, platform, and application teams.

The persisted agent workflow collects logs, metrics, traces, Git and tests; ranks falsifiable hypotheses; reproduces a failure; writes a regression; proposes a bounded patch; verifies it in Docker or a restricted local fallback; and stops at approval. Novelty comes from combining structured model decisions with deterministic state, patch policy, sandbox, verification and audit gates.

The Reliability Digital Twin finale raises that safety bar: a manifest pins the incident environment, three candidates run against identical conditions, counterfactual scenarios expose false fixes, blast-radius and evidence graphs disclose estimated impact and assumptions, and a deterministic adversarial reviewer challenges each patch. Mandatory gate failures disqualify candidates before scoring. The winning repair remains a recommendation until a human approves it.

The exportable incident package hashes each artifact and chains canonical audit events with SHA-256. Verification detects modification, but the package is described only as tamper-evident—not blockchain, formal proof, or legal non-repudiation.

Safety includes no automatic deployment, protected paths, command allowlists, isolated copied workspaces, network-disabled Docker, mandatory regression evidence, and approval-gated PR records. The demo uses only repository-owned synthetic e-commerce data and works offline with deterministic mock outputs. Current limits are SQLite, one fully repairable incident, simulated local PR records, and reduced Local Sandbox checks. Roadmap: PostgreSQL workers, real telemetry stores, GitHub Checks, ephemeral Kubernetes sandboxes, and additional repair templates.
