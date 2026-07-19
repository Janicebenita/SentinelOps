"""Bootstrap dependencies and launch the demo with a pip-capable interpreter."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
PYTHON_MODULES = ("fastapi", "httpx", "sqlalchemy", "uvicorn", "pytest")


def _candidate_pythons() -> list[str]:
    candidates = [
        sys.executable,
        shutil.which("python3"),
        shutil.which("python"),
        "/usr/local/python/current/bin/python",
        "/usr/local/bin/python3",
    ]
    unique: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in unique and Path(candidate).exists():
            unique.append(candidate)
    return unique


def _has_pip(python: str) -> bool:
    return subprocess.run(
        [python, "-m", "pip", "--version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def _python_with_pip() -> str | None:
    candidates = _candidate_pythons()
    for python in candidates:
        if _has_pip(python):
            return python
    for python in candidates:
        subprocess.run(
            [python, "-m", "ensurepip", "--upgrade"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if _has_pip(python):
            return python
    return None


def _modules_missing(python: str) -> list[str]:
    probe = ";".join(
        ["import importlib.util", f"names={PYTHON_MODULES!r}", "print(','.join(n for n in names if importlib.util.find_spec(n) is None))"]
    )
    result = subprocess.run([python, "-c", probe], text=True, capture_output=True, check=False)
    return result.stdout.strip().split(",") if result.stdout.strip() else []


def main() -> int:
    python = _python_with_pip()
    if python is None:
        print("No pip-capable Python interpreter is available in this environment.", file=sys.stderr)
        return 1
    missing = _modules_missing(python)
    if missing:
        print(f"Installing missing Python dependencies: {', '.join(missing)}")
        result = subprocess.run(
            [python, "-m", "pip", "install", "-e", ".[dev]"], cwd=ROOT, check=False
        )
        if result.returncode:
            return result.returncode

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if npm is None:
        print("npm is required", file=sys.stderr)
        return 1
    vite = ROOT / "frontend" / "node_modules" / ".bin" / ("vite.cmd" if os.name == "nt" else "vite")
    if not vite.exists():
        print("Installing missing frontend dependencies")
        result = subprocess.run([npm, "install"], cwd=ROOT / "frontend", check=False)
        if result.returncode:
            return result.returncode

    prepared = subprocess.run([python, "scripts/prepare_sandbox.py"], cwd=ROOT, check=False)
    if prepared.returncode:
        return prepared.returncode
    return subprocess.run([python, "scripts/run_demo.py"], cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
