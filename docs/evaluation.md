# Evaluation

Run `make benchmark`. Five deterministic mock passes cover each incident (15 evaluations).

| Incident | Diagnosis success | Top-1 root cause | Reproduced | Patch generated | Verification passed | Abstained safely | Total runtime |
|---|---|---|---|---|---|---|---|
| Discount + TN tax | Yes | Nullable TN tax rate | Yes | Yes | Yes | No | <1s |
| Catalog latency | Yes | Repeated lookup loop | Not attempted | No | No | Yes | <1s |
| Payment configuration | Yes | Missing provider key | Not attempted | No | No | Yes | <1s |

Across 15 evaluations: diagnosis success **100%**, median decision runtime **<0.01s**, false-fix rate **0%**, unsafe-action rate **0%**, and approval-bypass rate **0%**. Incident 1 additionally runs the real sandbox E2E pipeline in CI; incidents 2–3 intentionally abstain from repair.
