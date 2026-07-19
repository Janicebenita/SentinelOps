# Limitations

Incident 1 is the only complete automatic repair. Incidents 2–3 diagnose and abstain. SQLite and in-process orchestration are single-node MVP choices. Local Sandbox has weaker isolation and three pytest gates versus Docker's six. PRs are simulated unless GitHub credentials are configured. Provider fallback favors demo continuity and must be surfaced to operators. No production deployment is performed.
