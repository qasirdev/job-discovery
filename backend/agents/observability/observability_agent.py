import time
from contextlib import contextmanager
from typing import Generator, Any
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI
from ...logging_config import get_logger

logger = get_logger(__name__)


class ObservabilityAgent:
    """Manages system monitoring, OpenTelemetry tracing instrumentation, and performance profiling."""

    def __init__(self, service_name: str = "job-discovery-api") -> None:
        self.service_name = service_name
        self.tracer = self._setup_opentelemetry()

    def _setup_opentelemetry(self) -> trace.Tracer:
        """Initialize OpenTelemetry tracer provider and export pipelines."""
        logger.info(f"Initializing OpenTelemetry tracing for service: {self.service_name}")

        # Set up standard tracer provider
        provider = TracerProvider()

        # Export traces to console for visibility in local logging
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)

        # Set global tracer provider
        trace.set_tracer_provider(provider)
        return trace.get_tracer(self.service_name)

    def instrument_fastapi_app(self, app: FastAPI) -> None:
        """Register automated request tracing instrumentation on the FastAPI instance."""
        try:
            logger.info("Instrumenting FastAPI application with OpenTelemetry...")
            FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())
            logger.info("FastAPI OpenTelemetry instrumentation configured successfully.")
        except Exception as e:
            logger.error(f"Failed to instrument FastAPI application: {e}")

    @contextmanager
    def trace_agent_execution(self, agent_name: str) -> Generator[trace.Span, None, None]:
        """A context manager to trace and log time elapsed during child agent pipeline executions."""
        start_time = time.time()
        logger.info(f"[{agent_name}] Starting trace span...")

        with self.tracer.start_as_current_span(agent_name) as span:
            span.set_attribute("agent.name", agent_name)
            try:
                yield span
                duration = time.time() - start_time
                span.set_attribute("execution.duration_seconds", duration)
                span.set_attribute("execution.status", "success")
                logger.info(f"[{agent_name}] Completed successfully in {duration:.4f}s.")
            except Exception as e:
                duration = time.time() - start_time
                span.set_attribute("execution.duration_seconds", duration)
                span.set_attribute("execution.status", "error")
                span.set_attribute("error.message", str(e))
                logger.error(f"[{agent_name}] Execution failed after {duration:.4f}s: {e}")
                raise e

    def record_metric(self, name: str, value: Any, attributes: dict[str, Any] | None = None) -> None:
        """Log structured performance metrics for dashboard analysis."""
        attr_str = f" attributes={attributes}" if attributes else ""
        logger.info(f"[METRIC] {name}={value}{attr_str}")
