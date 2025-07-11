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

## Using with Local OTEL Collector

This project includes a local OpenTelemetry collector that receives traces and forwards them to LangSmith.

1. Start the local OTEL collector:
```bash
docker-compose up -d
```

2. Run the test script that sends traces to the local collector:
```bash
python test_otel.py
```

The local collector runs on `localhost:4318` (HTTP) and `localhost:4317` (gRPC), and automatically forwards traces to LangSmith using your configured API key.

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
- `test_otel.py` - Test script that sends traces to local OTEL collector
- `otel_config.py` - OpenTelemetry configuration
- `otel-collector-config.yaml` - OTEL collector configuration
- `docker-compose.yml` - Docker setup for local OTEL collector