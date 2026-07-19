"""Install launch dependencies only when the Codespace has not been prepared."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
PYTHON_MODULES = ("fastapi", "httpx", "sqlalchemy", "uvicorn", "pytest")


def main() -> int:
    missing = [name for name in PYTHON_MODULES if importlib.util.find_spec(name) is None]
    if missing:
        print(f"Installing missing Python dependencies: {', '.join(missing)}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            cwd=ROOT,
            check=False,
        )
        if result.returncode:
            return result.returncode

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if npm is None:
        print("npm is required", file=sys.stderr)
        return 1
    vite = ROOT / "frontend" / "node_modules" / ".bin" / ("vite.cmd" if sys.platform == "win32" else "vite")
    if not vite.exists():
        print("Installing missing frontend dependencies")
        result = subprocess.run([npm, "install"], cwd=ROOT / "frontend", check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
