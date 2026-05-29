import functools
from opentelemetry import trace

def trace_agent_run(agent_name: str, method_name: str = "run"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            tracer = trace.get_tracer(self.__module__)
            with tracer.start_as_current_span(f"{agent_name}.{method_name}") as span:
                span.set_attribute("agent_id", agent_name)
                return await func(self, *args, **kwargs)
        return wrapper
    return decorator
