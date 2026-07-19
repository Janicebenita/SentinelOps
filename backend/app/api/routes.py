from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..agent import workflow
from ..agent.state import AgentState
from ..database import get_db
from ..models import *
from ..schemas import ApprovalInput, IncidentCreate, IncidentRead
from ..services.audit import transition
router=APIRouter(prefix="/api")
def serialize(row): return {c.name:getattr(row,c.name) for c in row.__table__.columns}
@router.post("/incidents",response_model=IncidentRead)
def create(payload:IncidentCreate,db:Session=Depends(get_db)):
    row=Incident(**payload.model_dump()); db.add(row); db.commit(); db.refresh(row); return row
@router.get("/incidents")
def list_incidents(db:Session=Depends(get_db)): return [serialize(x) for x in db.scalars(select(Incident).order_by(Incident.id.desc()))]
@router.get("/incidents/{iid}")
def get_incident(iid:int,db:Session=Depends(get_db)): return serialize(workflow.require(db,iid))
@router.post("/incidents/{iid}/start")
def start(iid:int,db:Session=Depends(get_db)): return serialize(transition(db,workflow.require(db,iid),AgentState.ALERT_RECEIVED,actor="user"))
@router.post("/incidents/{iid}/collect-evidence")
def collect(iid:int,db:Session=Depends(get_db)): return [serialize(x) for x in workflow.collect_evidence(db,workflow.require(db,iid))]
@router.post("/incidents/{iid}/generate-hypotheses")
def gen_h(iid:int,db:Session=Depends(get_db)): return [serialize(x) for x in workflow.hypotheses(db,workflow.require(db,iid))]
@router.post("/incidents/{iid}/reproduce")
def repro(iid:int,db:Session=Depends(get_db)): return serialize(workflow.reproduce(db,workflow.require(db,iid)))
@router.post("/incidents/{iid}/generate-patch")
def patch(iid:int,db:Session=Depends(get_db)): return serialize(workflow.generate_patch(db,workflow.require(db,iid)))
@router.post("/incidents/{iid}/verify")
def verify(iid:int,db:Session=Depends(get_db)): return [serialize(x) for x in workflow.verify(db,workflow.require(db,iid))]
@router.post("/incidents/{iid}/approve")
def approve(iid:int,payload:ApprovalInput,db:Session=Depends(get_db)): workflow.approve(db,workflow.require(db,iid),payload.approved_by,True); return {"approved":True}
@router.post("/incidents/{iid}/reject")
def reject(iid:int,payload:ApprovalInput,db:Session=Depends(get_db)): workflow.approve(db,workflow.require(db,iid),payload.approved_by,False); return {"approved":False}
@router.post("/incidents/{iid}/create-pr")
def pr(iid:int,db:Session=Depends(get_db)):
    try:return serialize(workflow.create_pr(db,workflow.require(db,iid)))
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
def listing(model,iid,db): return [serialize(x) for x in db.scalars(select(model).where(model.incident_id==iid))]
@router.get("/incidents/{iid}/evidence")
def evidence(iid:int,db:Session=Depends(get_db)): return listing(EvidenceItem,iid,db)
@router.get("/incidents/{iid}/hypotheses")
def hyp(iid:int,db:Session=Depends(get_db)): return listing(Hypothesis,iid,db)
@router.get("/incidents/{iid}/patches")
def patches(iid:int,db:Session=Depends(get_db)): return listing(PatchCandidate,iid,db)
@router.get("/incidents/{iid}/pull-requests")
def pull_requests(iid:int,db:Session=Depends(get_db)): return listing(PullRequestRecord,iid,db)
@router.get("/incidents/{iid}/verification")
def verification(iid:int,db:Session=Depends(get_db)):
    ids=select(PatchCandidate.id).where(PatchCandidate.incident_id==iid); return [serialize(x) for x in db.scalars(select(VerificationRun).where(VerificationRun.patch_candidate_id.in_(ids)))]
@router.get("/incidents/{iid}/timeline")
@router.get("/incidents/{iid}/audit-log")
def timeline(iid:int,db:Session=Depends(get_db)): return listing(AuditEvent,iid,db)
@router.post("/demo/seed")
def seed(db:Session=Depends(get_db)):
    if db.scalar(select(Incident).limit(1)): return {"seeded":False,"reason":"already seeded"}
    rows=[Incident(title="Discount + TN tax causes checkout 500",description="SAVE10 orders in TN fail during tax arithmetic",severity="SEV1"),Incident(title="Catalog latency regression",description="Recent commit repeats product lookup in a loop",severity="SEV2"),Incident(title="Payment startup configuration missing",description="PAYMENT_PROVIDER_KEY is absent",severity="SEV2")]; db.add_all(rows); db.commit(); return {"seeded":True,"ids":[r.id for r in rows]}
@router.post("/demo/trigger-incident")
def trigger(db:Session=Depends(get_db)):
    row=db.scalar(select(Incident).order_by(Incident.id));
    if row is None: raise HTTPException(404,"Seed an incident first")
    if row.current_state=="NEW": transition(db,row,AgentState.ALERT_RECEIVED,actor="demo-alert")
    return serialize(row)
@router.post("/demo/generate-traffic")
def traffic(): return {"generated":True,"message":"Use scripts/generate_traffic.py against the demo app"}
@router.post("/demo/reset")
def reset(db:Session=Depends(get_db)):
    for model in [PullRequestRecord,AuditEvent,ApprovalRequest,VerificationRun,PatchCandidate,ReproductionAttempt,Hypothesis,EvidenceItem,Incident]: db.execute(__import__('sqlalchemy').delete(model))
    db.commit(); return {"reset":True}
