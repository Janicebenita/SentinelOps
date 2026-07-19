# 3 minute 40 second demo

- **0:00–0:20** Open Sentinel Shop health/products and the green operations dashboard.
- **0:20–0:40** Run `python scripts/generate_traffic.py`; show TN + SAVE10 returning 500 and the error-rate/latency spike.
- **0:40–1:10** Trigger Incident 1 and advance evidence collection; open logs, metrics, trace span, recent commits, and the immutable audit timeline.
- **1:10–1:40** Show three ranked hypotheses. Point out the 94% nullable TN tax-rate hypothesis and specific evidence for and against it.
- **1:40–2:05** Advance reproduction. Show the generated regression and its required before-patch HTTP 500 failure.
- **2:05–2:35** Show the one-line normalization diff, two-file boundary, low risk score, and restricted sandbox controls.
- **2:35–3:00** Run verification. Show regression, unit, integration, Ruff, MyPy, and Bandit checks plus rollback plan.
- **3:00–3:20** Emphasize that the agent is stopped at `AWAITING_APPROVAL`; click Approve PR as the operator.
- **3:20–3:40** Create the local draft PR record and show branch name, commit identifier, report, audit completion, and recovered metrics. State explicitly: SentinelOps did not deploy.
