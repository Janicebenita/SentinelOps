# Exact three-minute demo

- **0:00–0:20:** Open port 5173. Point to Demo Ready, SEV1, detected time, 34.2% error rate and 182ms latency.
- **0:20–0:35:** Select Incident 1 and click **Run Autonomous Investigation** once.
- **0:35–1:05:** Watch trigger, evidence, hypothesis and reproduction stages complete; call out four evidence artifacts and 94% confidence.
- **1:05–1:35:** Show “Failed before patch ✓”, the nullable-rate patch summary, and the real isolated verification stage.
- **1:35–2:05:** Show passing regression/unit/integration (and Docker quality gates), recovered error/latency cards, and persisted state.
- **2:05–2:25:** Emphasize the stop at **Human approval required**; explain that PR creation returns 409 before approval.
- **2:25–2:45:** Click **Approve PR**, then create the approved local PR record. State that nothing deploys automatically.
- **2:45–3:00:** Show the PR status, audit trail, screenshot-state query, and **Reset Demo** for deterministic replay.
