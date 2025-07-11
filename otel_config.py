"""OpenTelemetry configuration for pydantic-ai with LangSmith integration."""

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor


def setup_otel_tracing():
    """Configure OpenTelemetry tracing to send to LangSmith."""
    os.environ["LANGSMITH_OTEL_ENABLED"] = "true"
    # Get LangSmith API key from environment
    langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
    if not langsmith_api_key:
        raise ValueError("LANGSMITH_API_KEY environment variable is required")
    
    # Optional: specify project name
    langsmith_project = os.getenv("LANGSMITH_PROJECT", "pydantic-ai-demo")
    
    # Set up tracer provider
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    # Configure OTLP exporter for LangSmith
    headers = {
        "x-api-key": langsmith_api_key,
        "Langsmith-Project": langsmith_project
    }
    
    otlp_exporter = OTLPSpanExporter(
        endpoint="https://api.smith.langchain.com/otel/v1/traces",
        headers=headers
    )
    
    # Add batch span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Instrument HTTP libraries
    RequestsInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    
    return tracer


def shutdown_otel():
    """Gracefully shutdown OpenTelemetry."""
    tracer_provider = trace.get_tracer_provider()
    if hasattr(tracer_provider, 'shutdown'):
        tracer_provider.shutdown()