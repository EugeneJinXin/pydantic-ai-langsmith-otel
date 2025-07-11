"""Simple test script to send traces via OTEL collector to LangSmith."""

import time
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

load_dotenv()

# Configure to send to local OTEL collector
trace.set_tracer_provider(TracerProvider())

# Send to local collector (which will forward to LangSmith)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",
    headers={}  # No headers needed for local collector
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

def main():
    """Send a test trace."""
    with tracer.start_as_current_span("test-trace") as span:
        span.set_attribute("test.message", "Hello from OTEL collector test")
        span.set_attribute("test.timestamp", int(time.time()))
        
        print("Sending test trace to local OTEL collector...")
        
        # Simulate some work
        time.sleep(0.1)
        
        with tracer.start_as_current_span("child-span") as child_span:
            child_span.set_attribute("operation", "test-operation")
            time.sleep(0.05)
    
    # Force flush
    trace.get_tracer_provider().shutdown()
    print("Test trace sent!")

if __name__ == "__main__":
    main()