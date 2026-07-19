FROM python:3.12-slim
RUN useradd --create-home --uid 10001 runner
WORKDIR /workspace
COPY pyproject.toml /tmp/pyproject.toml
RUN pip install --no-cache-dir "/tmp[dev]"
COPY sandbox/entrypoint.py /opt/entrypoint.py
USER runner
ENTRYPOINT ["python", "/opt/entrypoint.py"]
