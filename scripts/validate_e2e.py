"""Exercise the seeded incident and assert every deterministic safety gate."""

from __future__ import annotations

import hashlib
from pathlib import Path

import httpx

from backend.app.tools.patch_tools import PatchPolicyError, inspect_patch

API = "http://localhost:8000/api"
BUG = {"items": [{"product_id": 1, "quantity": 2}], "discount_code": "SAVE10", "region": "TN"}

def source_hash() -> str:
    return hashlib.sha256(Path("demo_app/app/main.py").read_bytes()).hexdigest()

def main() -> int:
    with httpx.Client(timeout=180) as client:
        client.post(f"{API}/demo/reset").raise_for_status()
        seed = client.post(f"{API}/demo/seed"); seed.raise_for_status(); incident_id = seed.json()["ids"][0]
        failure = client.post("http://localhost:8001/checkout", json=BUG)
        assert failure.status_code == 500
        client.post(f"{API}/incidents/{incident_id}/start").raise_for_status()
        client.post(f"{API}/incidents/{incident_id}/collect-evidence").raise_for_status()
        client.post(f"{API}/incidents/{incident_id}/generate-hypotheses").raise_for_status()
        hypotheses = client.get(f"{API}/incidents/{incident_id}/hypotheses").json()
        assert hypotheses[0]["title"] == "Nullable TN tax rate in discounted checkout"
        reproduction = client.post(f"{API}/incidents/{incident_id}/reproduce"); reproduction.raise_for_status()
        assert reproduction.json()["result"] == "confirmed"
        client.post(f"{API}/incidents/{incident_id}/generate-patch").raise_for_status()
        before = source_hash()
        verification = client.post(f"{API}/incidents/{incident_id}/verify"); verification.raise_for_status()
        assert source_hash() == before
        assert all(check["passed"] for check in verification.json())
        assert client.post(f"{API}/incidents/{incident_id}/create-pr").status_code == 409
        evidence = client.get(f"{API}/incidents/{incident_id}/evidence").json()
        assert {item["evidence_type"] for item in evidence} >= {"log", "metric", "trace", "git"}
        audit = client.get(f"{API}/incidents/{incident_id}/audit-log").json()
        assert len(audit) >= 10
        try: inspect_patch("+unsafe", ["sandbox/Dockerfile"], True)
        except PatchPolicyError: pass
        else: raise AssertionError("protected path policy did not reject patch")
        client.post(f"{API}/incidents/{incident_id}/approve", json={"approved_by": "e2e-operator"}).raise_for_status()
        client.post(f"{API}/incidents/{incident_id}/create-pr").raise_for_status()
    print("Seeded incident passed every evidence, sandbox, policy, approval, and audit assertion")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
