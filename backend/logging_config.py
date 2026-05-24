import logging
import sys
import contextvars
import structlog
from typing import Any

request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")

def add_request_id(logger: logging.Logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    req_id = request_id_ctx.get()
    if req_id:
        event_dict["request_id"] = req_id
    return event_dict

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        add_request_id,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

def get_logger(name: str) -> structlog.BoundLogger:
    """Return a configured structured JSON logger using structlog."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    return structlog.get_logger(name)
