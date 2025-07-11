# Pydantic-AI with LangSmith OpenTelemetry Integration

This project demonstrates how to set up pydantic-ai with OpenTelemetry tracing that sends data to LangSmith.

## Problem & Solution

The original configuration had two issues:
1. **Incorrect endpoint**: Used `https://api.smith.langchain.com:443/otel` instead of `https://api.smith.langchain.com/otel`
2. **Case-sensitive header**: Used `'Langsmith-Project'` instead of the proper casing

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the example:
```bash
python main.py
```

## Using with OTEL Collector

1. Start the collector:
```bash
docker-compose up -d
```

2. Configure your application to send traces to the collector at `localhost:4318`

## Key Configuration Changes

**Corrected OTEL Collector Config:**
```yaml
exporters:
  otlphttp/langsmith:
    endpoint: 'https://api.smith.langchain.com/otel'  # No port :443
    headers:
      'x-api-key': '${LANGSMITH_API_KEY}'  # lowercase 'x'
      'Langsmith-Project': '${LANGSMITH_PROJECT}'
```

**Python Configuration:**
```python
otlp_exporter = OTLPSpanExporter(
    endpoint="https://api.smith.langchain.com/otel/v1/traces",
    headers={"x-api-key": langsmith_api_key}
)
```

## Files

- `main.py` - Example pydantic-ai agent with tracing
- `otel_config.py` - OpenTelemetry configuration
- `otel-collector-config.yaml` - OTEL collector configuration
- `docker-compose.yml` - Docker setup for OTEL collector