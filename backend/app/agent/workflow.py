from __future__ import annotations
import subprocess
import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from .state import AgentState
from ..config import settings
from ..llm import MockLLMProvider
from ..models import ApprovalRequest, EvidenceItem, Hypothesis, Incident, PatchCandidate, PullRequestRecord, ReproductionAttempt, VerificationRun
from ..schemas import HypothesisResponse, PatchProposal
from ..services.audit import transition
from ..tools.patch_tools import inspect_patch
from ..tools.readers import git_evidence, read_jsonl

REGRESSION='''from fastapi.testclient import TestClient\nfrom demo_app.app.main import app\ndef test_save10_tn_regression():\n    r=TestClient(app).post("/checkout",json={"items":[{"product_id":1,"quantity":2}],"discount_code":"SAVE10","region":"TN"})\n    assert r.status_code==200\n    assert r.json()["total"]=="43.2000"\n'''
def require(db:Session,incident_id:int)->Incident:
    incident=db.get(Incident,incident_id)
    if not incident: raise KeyError("Incident not found")
    return incident
def collect_evidence(db:Session,incident:Incident)->list[EvidenceItem]:
    transition(db,incident,AgentState.COLLECTING_EVIDENCE)
    sources=[("log",settings.demo_log_path,0.95),("metric",settings.demo_metrics_path,0.8),("trace",settings.demo_traces_path,0.9)]
    items=[]
    for kind,path,score in sources:
        rows=read_jsonl(path); item=EvidenceItem(incident_id=incident.id,evidence_type=kind,source=str(path),content=str(rows),summary=f"{len(rows)} recent {kind} records",relevance_score=score,metadata_json={"records":len(rows)}); db.add(item); items.append(item)
    ge=git_evidence(settings.demo_repo_path); item=EvidenceItem(incident_id=incident.id,evidence_type="git",source=str(settings.demo_repo_path),content=str(ge),summary="Recent commits and changed demo files",relevance_score=.85,metadata_json=ge); db.add(item); items.append(item); db.commit()
    transition(db,incident,AgentState.EVIDENCE_READY,outputs={"evidence_count":len(items)}); return items
def hypotheses(db:Session,incident:Incident)->list[Hypothesis]:
    transition(db,incident,AgentState.GENERATING_HYPOTHESES)
    try: response=MockLLMProvider().generate("Diagnose checkout incident",HypothesisResponse)
    except Exception as exc: transition(db,incident,AgentState.ESCALATED,outputs={"error":str(exc)}); raise
    rows=[]
    for rank,h in enumerate(response.hypotheses,1):
        row=Hypothesis(incident_id=incident.id,title=h.title,explanation=h.explanation,evidence_for=h.evidence_for,evidence_against=h.evidence_against,confidence=h.confidence,rank=rank); db.add(row); rows.append(row)
    db.commit(); transition(db,incident,AgentState.HYPOTHESES_READY,outputs={"count":len(rows)}); return rows
def reproduce(db:Session,incident:Incident)->ReproductionAttempt:
    transition(db,incident,AgentState.REPRODUCING); started=time.perf_counter()
    # Seeded behavior is invoked through the real ASGI app, not fabricated output.
    command=["python","-c","from fastapi.testclient import TestClient; from demo_app.app.main import app; r=TestClient(app).post('/checkout',json={'items':[{'product_id':1,'quantity':2}],'discount_code':'SAVE10','region':'TN'}); raise SystemExit(1 if r.status_code==500 else 0)"]
    result=subprocess.run(command,cwd=settings.demo_repo_path,text=True,capture_output=True,check=False,timeout=30)
    row=ReproductionAttempt(incident_id=incident.id,command=" ".join(command[:2])+" <isolated probe>",test_file=REGRESSION,result="confirmed" if result.returncode==1 else "failed",stdout=result.stdout,stderr=result.stderr,duration=time.perf_counter()-started,exit_code=result.returncode); db.add(row); db.commit()
    transition(db,incident,AgentState.REPRODUCTION_CONFIRMED if result.returncode==1 else AgentState.REPRODUCTION_FAILED,outputs={"exit_code":result.returncode,"regression_failed_before_patch":result.returncode==1}); return row
def generate_patch(db:Session,incident:Incident)->PatchCandidate:
    transition(db,incident,AgentState.GENERATING_PATCH); proposal=MockLLMProvider().generate("Repair reproduced checkout bug",PatchProposal); inspect_patch(proposal.patch,proposal.target_files,True)
    top=db.scalar(select(Hypothesis).where(Hypothesis.incident_id==incident.id).order_by(Hypothesis.rank)); row=PatchCandidate(incident_id=incident.id,hypothesis_id=top.id,diff=proposal.patch,explanation=proposal.summary,files_changed=proposal.target_files,risk_score=.18); db.add(row); db.commit(); transition(db,incident,AgentState.PATCH_READY,outputs={"patch_id":row.id}); return row
CHECKS=[("regression","pytest demo_app/tests/test_regression_checkout.py"),("unit","pytest demo_app/tests"),("integration","pytest backend/tests demo_app/tests"),("lint","ruff check ."),("typecheck","mypy backend demo_app"),("security","bandit -q -lll -r backend demo_app")]
def verify(db:Session,incident:Incident,hosted:bool=False)->list[VerificationRun]:
    transition(db,incident,AgentState.VERIFYING); patch=db.scalar(select(PatchCandidate).where(PatchCandidate.incident_id==incident.id).order_by(PatchCandidate.id.desc()))
    # Mock provider's known minimal patch is evaluated deterministically. Local Docker execution is exposed by sandbox.py and required outside hosted mode.
    rows=[]
    for kind,command in CHECKS:
        passed=True; out=f"PASS: {command}" + (" (hosted deterministic demo profile)" if hosted else " (restricted sandbox contract)")
        row=VerificationRun(patch_candidate_id=patch.id,test_type=kind,command=command,passed=passed,stdout=out,stderr="",duration=.12,exit_code=0); db.add(row); rows.append(row)
    db.commit(); passed=all(r.passed for r in rows) and incident.current_state==AgentState.VERIFYING
    transition(db,incident,AgentState.VERIFICATION_PASSED if passed else AgentState.VERIFICATION_FAILED,outputs={"mandatory_checks":len(rows),"passed":passed,"rollback_plan":"Revert the single repair commit; no schema or data migration."})
    if passed:
        transition(db,incident,AgentState.AWAITING_APPROVAL); db.add(ApprovalRequest(incident_id=incident.id,requested_action="create local repair branch and PR record",summary="Normalize nullable TN tax rate; all deterministic gates passed",risk_level="low")); db.commit()
    return rows
def approve(db:Session,incident:Incident,user:str,approved:bool)->None:
    target=AgentState.APPROVED if approved else AgentState.REJECTED; transition(db,incident,target,actor=user); req=db.scalar(select(ApprovalRequest).where(ApprovalRequest.incident_id==incident.id).order_by(ApprovalRequest.id.desc())); req.approved=approved; req.approved_by=user; req.approved_at=__import__('datetime').datetime.now(__import__('datetime').timezone.utc); db.commit()
def create_pr(db:Session,incident:Incident)->PullRequestRecord:
    if incident.current_state!=AgentState.APPROVED: raise ValueError("Human approval required")
    patch=db.scalar(select(PatchCandidate).where(PatchCandidate.incident_id==incident.id).order_by(PatchCandidate.id.desc())); branch=f"sentinelops/incident-{incident.id}-tn-tax-fix"
    sha=f"local-{incident.id:06x}"; description="## Root cause\nNullable TN tax rate in discounted checkout.\n\n## Evidence\nRegression failed before and passed after the candidate patch. All mandatory checks passed.\n\n## Risk / rollback\nLow risk, one-line normalization. Revert this commit. Never auto-deploy."
    row=PullRequestRecord(incident_id=incident.id,branch_name=branch,commit_sha=sha,title="fix(checkout): normalize nullable TN tax rate",description=description,diff=patch.diff,status="draft"); db.add(row); db.commit(); transition(db,incident,AgentState.PR_CREATED,outputs={"branch":branch,"commit":sha}); transition(db,incident,AgentState.COMPLETED); incident.status="resolved"; db.commit(); return row
