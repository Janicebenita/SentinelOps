# Limitations

Incident 1 is the only complete automatic repair. Incidents 2–3 diagnose and abstain. SQLite and in-process orchestration are single-node MVP choices. Local Sandbox has weaker isolation and three pytest gates versus Docker's six. PRs are simulated unless GitHub credentials are configured. Provider fallback favors demo continuity and must be surfaced to operators. No production deployment is performed.
# Finale limitations

- The checkout twin uses deterministic repository-owned fixtures rather than a production container snapshot or live telemetry store.
- Counterfactual outcomes model the seeded service and are not a general causal simulator.
- Blast-radius confidence is limited by static relationships and curated demo coverage.
- Fault-injection and dependency-impact checks use deterministic fallbacks when optional external tools are unavailable; the UI labels reduced assurance.
- SQLite and in-process execution are appropriate for a single demo instance, not distributed production orchestration.
- The evidence package provides tamper evidence, not authenticity of the original collector, formal proof, blockchain guarantees, or legal non-repudiation.
- Only Incident 1 supports the complete repair tournament. Incidents 2 and 3 remain diagnostic demonstrations.
- Approval produces a local PR report. Nothing is automatically deployed.

Production evolution should use PostgreSQL, an object store, signed collector identities, OpenTelemetry storage, ephemeral Kubernetes jobs with immutable images, a real coverage/call graph, calibrated confidence, and GitHub Checks integration.
