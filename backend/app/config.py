from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./data/sentinelops.db"
    llm_provider: str = "mock"
    demo_repo_path: Path = Path(".")
    demo_log_path: Path = Path("data/logs/demo.jsonl")
    demo_metrics_path: Path = Path("data/metrics/demo.jsonl")
    demo_traces_path: Path = Path("data/traces/demo.jsonl")
    sandbox_image: str = "sentinelops-sandbox:latest"
settings = Settings()
