from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router
from .database import Base,engine
Base.metadata.create_all(engine)
app=FastAPI(title="SentinelOps API",version="0.1.0",description="Evidence-driven, approval-gated AI reliability engineer")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
@app.get("/health")
def health(): return {"status":"ok","provider":"mock","auto_deploy":False}
