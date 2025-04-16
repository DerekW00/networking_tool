FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY apps/collector/pyproject.toml apps/collector/
COPY libs/common/pyproject.toml libs/common/

# Install common library first
WORKDIR /app/libs/common
RUN pip install --no-cache-dir -e .

# Install collector app
WORKDIR /app/apps/collector
RUN pip install --no-cache-dir -e .

# Copy source code
COPY libs/common/src/ /app/libs/common/src/
COPY apps/collector/src/ /app/apps/collector/src/
COPY configs/ /app/configs/

# Create data directories
RUN mkdir -p /app/data/raw /app/data/interim

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the collector
WORKDIR /app
ENTRYPOINT ["python", "-m", "collector"]
CMD ["--config", "/app/configs/prod/collector.yaml"] 