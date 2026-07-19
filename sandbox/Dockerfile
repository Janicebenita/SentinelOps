FROM python:3.12-slim
RUN useradd --create-home --uid 10001 runner
WORKDIR /workspace
RUN pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings sqlalchemy httpx \
    python-json-logger pyyaml pytest pytest-cov ruff mypy bandit
COPY sandbox/entrypoint.py /opt/entrypoint.py
USER runner
ENTRYPOINT ["python", "/opt/entrypoint.py"]
