import pytest
from backend.app.tools.patch_tools import PatchPolicyError, inspect_patch
from backend.app.tools.sandbox import validate_command

def test_safe_patch():
    assert inspect_patch("-x\n+y", ["demo_app/app/main.py", "demo_app/tests/test_regression.py"], True)["within_policy"]

def test_protected_patch():
    with pytest.raises(PatchPolicyError):
        inspect_patch("+x", ["sandbox/Dockerfile"], True)

def test_command_allowlist():
    validate_command(["pytest", "-q"])
    with pytest.raises(ValueError):
        validate_command(["curl", "example.com"])
    with pytest.raises(ValueError):
        validate_command(["pytest", "-q;whoami"])
