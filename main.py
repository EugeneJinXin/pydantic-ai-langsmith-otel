"""Example pydantic-ai agent with OpenTelemetry tracing to LangSmith."""

import asyncio
import os
from dotenv import load_dotenv
from opentelemetry import trace
from pydantic_ai import Agent
from otel_config import setup_otel_tracing, shutdown_otel

# Load environment variables from .env file
load_dotenv()


# Initialize OpenTelemetry tracing
tracer = setup_otel_tracing()

# Create a simple pydantic-ai agent
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt='You are a helpful assistant that answers questions concisely.',
)


async def main():
    """Run example agent with tracing."""
    with tracer.start_as_current_span("pydantic-ai-example") as span:
        span.set_attribute("agent.model", "gpt-4o-mini")
        span.set_attribute("agent.system_prompt", "helpful assistant")
        
        try:
            # Run the agent
            result = await agent.run("What is the capital of France?")
            
            span.set_attribute("agent.response", str(result.output))
            span.set_attribute("agent.success", True)
            
            print(f"Agent response: {result.output}")
            
        except Exception as e:
            span.set_attribute("agent.error", str(e))
            span.set_attribute("agent.success", False)
            raise
        finally:
            # Ensure traces are sent before shutdown
            shutdown_otel()


if __name__ == "__main__":
    # Ensure required environment variables are set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)
    
    if not os.getenv("LANGSMITH_API_KEY"):
        print("Please set LANGSMITH_API_KEY environment variable")
        exit(1)
    
    asyncio.run(main())
