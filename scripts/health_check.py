"""Verify that every SentinelOps demo service is accepting requests."""

from __future__ import annotations

import sys
import time

import httpx

SERVICES = {
    "frontend": "http://localhost:5173/",
    "backend": "http://localhost:8000/health",
    "demo_app": "http://localhost:8001/health",
}

def main() -> int:
    failures: list[str] = []
    with httpx.Client(timeout=2) as client:
        for name, url in SERVICES.items():
            error = "not checked"
            for _ in range(20):
                try:
                    response = client.get(url)
                    response.raise_for_status()
                    print(f"{name}: healthy ({url})")
                    break
                except httpx.HTTPError as exc:
                    error = str(exc)
                    time.sleep(0.5)
            else:
                failures.append(f"{name}: {error}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
