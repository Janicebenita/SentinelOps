from __future__ import annotations
import re
import subprocess
import time
from dataclasses import dataclass
ALLOWED={"pytest","python","ruff","mypy","bandit","git"}; META=re.compile(r"[;&|`$<>\n\r]")
@dataclass
class CommandResult: stdout:str; stderr:str; exit_code:int; duration:float; timed_out:bool=False
def validate_command(command:list[str])->None:
    if not command or command[0] not in ALLOWED: raise ValueError("Command is not allowlisted")
    if any(META.search(arg) for arg in command): raise ValueError("Shell metacharacters are forbidden")
    if command[0]=="git" and (len(command)<2 or command[1] not in {"diff","status","show"}): raise ValueError("Git command is not read-only")
def docker_run(command:list[str],workspace:str,image:str="sentinelops-sandbox:latest",timeout:int=90)->CommandResult:
    validate_command(command); started=time.perf_counter()
    docker=["docker","run","--rm","--network=none","--cpus=1","--memory=512m","--pids-limit=128","--read-only","--tmpfs","/tmp:rw,noexec,nosuid,size=128m","-v",f"{workspace}:/workspace:rw","-w","/workspace",image,*command]
    try:
        result=subprocess.run(docker,text=True,capture_output=True,timeout=timeout,check=False)
        return CommandResult(result.stdout,result.stderr,result.returncode,time.perf_counter()-started)
    except OSError as exc:
        return CommandResult("",f"Sandbox unavailable: {exc}",127,time.perf_counter()-started)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return CommandResult(stdout,stderr,124,time.perf_counter()-started,True)
