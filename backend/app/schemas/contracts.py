from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class IncidentCreate(BaseModel):
    title:str; description:str=""; severity:str="SEV2"; source:str="demo"; service_name:str="sentinel-shop"
class IncidentRead(IncidentCreate):
    model_config=ConfigDict(from_attributes=True); id:int; status:str; current_state:str; created_at:datetime; updated_at:datetime
class HypothesisDecision(BaseModel):
    title:str; explanation:str; evidence_for:list[str]=Field(min_length=1); evidence_against:list[str]; confidence:float=Field(ge=0,le=1); relevant_files:list[str]
class HypothesisResponse(BaseModel): hypotheses:list[HypothesisDecision]=Field(min_length=2,max_length=3)
class PatchProposal(BaseModel):
    summary:str; target_files:list[str]=Field(min_length=1,max_length=5); patch:str; expected_effect:str; risks:list[str]; verification_plan:list[str]
class ApprovalInput(BaseModel): approved_by:str=Field(min_length=2,max_length=100)
