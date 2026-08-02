# Exact three-minute demo

- **0:00–0:20:** Open port 5173. Point to Demo Ready, SEV1, detected time, 34.2% error rate and 182ms latency.
- **0:20–0:35:** Select Incident 1 and click **Run Autonomous Investigation** once.
- **0:35–1:05:** Watch trigger, evidence, hypothesis and reproduction stages complete; call out four evidence artifacts and 94% confidence.
- **1:05–1:35:** Show “Failed before patch ✓”, the nullable-rate patch summary, and the real isolated verification stage.
- **1:35–2:05:** Show passing regression/unit/integration (and Docker quality gates), recovered error/latency cards, and persisted state.
- **2:05–2:25:** Emphasize the stop at **Human approval required**; explain that PR creation returns 409 before approval.
- **2:25–2:45:** Click **Approve PR**, then create the approved local PR record. State that nothing deploys automatically.
- **2:45–3:00:** Show the PR status, audit trail, screenshot-state query, and **Reset Demo** for deterministic replay.
# Three-minute finale demo

- **0:00–0:15** Show healthy Sentinel Shop and Command Center. Say: “SentinelOps does not merely generate fixes. It proves which repair is safest before a human approves it.”
- **0:15–0:30** Trigger TN + `SAVE10`; show HTTP 500 and telemetry spike.
- **0:30–0:55** Start investigation; open linked logs, metrics, traces, Git evidence, and falsifiable hypotheses.
- **0:55–1:15** Open Digital Twin; show manifest hash, fixed seed, disabled network, and three identical failure replays.
- **1:15–1:40** Open Repair Tournament; compare A, B, and C across the gate matrix.
- **1:40–2:05** Open Counterfactual Lab; show A failing TN without discount and B changing the missing-rate contract.
- **2:05–2:25** Show Candidate C's 18/100 estimated blast radius, causal evidence graph, and adversarial review.
- **2:25–2:45** Show deterministic gates and the safety strip: source changed No, automatic deployment No, human approval Yes.
- **2:45–3:00** Approve, create the PR report and tamper-evident package, then say: “SentinelOps turns AI-generated repair into evidence-proven, human-controlled reliability engineering.”

Deterministic screenshot states: `?demoState=incident`, `evidence`, `hypothesis`, `twin`, `tournament`, `counterfactual`, `blast-radius`, `approval`, and `completed`.
