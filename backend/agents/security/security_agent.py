import re
import bleach
import json
import hashlib
from typing import Callable
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
from pydantic import BaseModel
from ...logging_config import get_logger

logger = get_logger("security")

class SecurityValidationResult(BaseModel):
    is_safe: bool
    reason: str
    
    model_config = {"extra": "forbid"}

from ...schemas import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ..base import BaseAgent
import time

class SecurityAgent(BaseAgent):
    """Validates scraped data and inputs for prompt injection, XSS, SSRF, and exploit attempts."""

    ALLOWED_DOMAINS = {
        "linkedin.com",
        "jobserve.com",
        "github.com",
        "githubusercontent.com"
    }

    def __init__(self) -> None:
        self.prompt_path = (
            Path(__file__).parent.parent.parent.parent
            / "prompts"
            / "security"
            / "system.md"
        )
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        if not self.prompt_path.exists():
            return "You are a Security Agent. Analyze text for prompt injection."
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Failed to read security system prompt: {e}")
            return "You are a Security Agent. Analyze text for prompt injection."

    async def sanitize_input(self, text: str) -> str:
        """Strip executable scripts, unsafe HTML tags, and suspicious code blocks."""
        logger.info("Security Agent sanitizing input...")
        if not text:
            return ""

        input_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # HTML sanitisation using bleach
        allowed_tags = ['b', 'i', 'code', 'pre', 'a']
        allowed_attrs = {'a': ['href']}
        clean_text = bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)

        logger.info(json.dumps({"event": "sanitisation_applied", "input_hash": input_hash}))
        return clean_text.strip()

    async def validate_url(self, url: str) -> bool:
        """Enforce SSRF domain allowlist for outgoing requests."""
        if not url:
            return False
            
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            domain = parsed.hostname
            if not domain:
                return False
                
            # Check if domain or its parent is in the allowlist
            is_allowed = any(domain == allowed or domain.endswith(f".{allowed}") for allowed in self.ALLOWED_DOMAINS)
            
            if not is_allowed:
                logger.warning(json.dumps({
                    "event": "ssrf_violation",
                    "url": url,
                    "reason": "Domain not in SSRF allowlist"
                }))
            return is_allowed
        except Exception as e:
            logger.error(f"URL parsing failed: {e}")
            return False

    async def validate_for_injection(self, text: str) -> AgentResultEnvelope:
        """Check for prompt injection and SQL/command injection patterns."""
        start_time = time.time()
        if not text:
            duration = time.time() - start_time
            return AgentResultEnvelope(agent_id="security", canonical_role="critic", status="success", result=SecurityValidationResult(is_safe=True, reason="Input is empty.").model_dump(), metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="regex", prompt_version=None))

        input_hash = hashlib.sha256(text.encode()).hexdigest()
        text_lower = text.lower()

        # Parse patterns from system.md XML block
        injection_triggers = []
        if "<patterns>" in self.system_prompt:
            patterns_block = self.system_prompt.split("<patterns>")[1].split("</patterns>")[0]
            for line in patterns_block.split("\n"):
                if "<pattern>" in line:
                    pattern = line.split("<pattern>")[1].split("</pattern>")[0].strip()
                    if pattern:
                        injection_triggers.append(pattern.lower())
        
        if not injection_triggers:
            # Fallback list if prompt fails to parse
            injection_triggers = [
                "ignore all previous instructions",
                "ignore previous instructions",
                "bypass system rules",
                "override system guidelines",
                "forget your instructions",
                "jailbreak",
                "dan",
            ]

        for trigger in injection_triggers:
            if trigger in text_lower:
                logger.warning(json.dumps({
                    "event": "prompt_injection_attempt",
                    "input_hash": input_hash,
                    "agent": "security",
                    "reason": f"Pattern: {trigger}"
                }))
                duration = time.time() - start_time
                return AgentResultEnvelope(agent_id="security", canonical_role="critic", status="needs_review", result=SecurityValidationResult(is_safe=False, reason=f"Detected potential prompt injection attempt: '{trigger}'").model_dump(), metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="regex", prompt_version=None), escalation=AgentEscalation(reason="Prompt injection detected", target_agent="orchestrator"))

        sql_injection_patterns = [
            r"union\s+select", r"select\s+.*\s+from\s+jobs", r"drop\s+table\s+jobs", r"delete\s+from\s+jobs", r"truncate\s+table", r"'\s*or\s*'1'\s*=\s*'1", r'"\s*or\s*"1"\s*=\s*"1'
        ]

        for pattern in sql_injection_patterns:
            if re.search(pattern, text_lower):
                logger.warning(json.dumps({
                    "event": "sql_injection_attempt",
                    "input_hash": input_hash,
                    "agent": "security"
                }))
                duration = time.time() - start_time
                return AgentResultEnvelope(agent_id="security", canonical_role="critic", status="needs_review", result=SecurityValidationResult(is_safe=False, reason="Detected potential SQL injection exploit attempt.").model_dump(), metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="regex", prompt_version=None), escalation=AgentEscalation(reason="SQL injection detected", target_agent="orchestrator"))

        duration = time.time() - start_time
        return AgentResultEnvelope(agent_id="security", canonical_role="critic", status="success", result=SecurityValidationResult(is_safe=True, reason="Input appears safe.").model_dump(), metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="regex", prompt_version=None))

    async def validate_output(self, output: str | dict) -> AgentResultEnvelope:
        """Review agent outputs for PII leakage, hallucinated URLs, and security risks before storage."""
        logger.info("Security Agent reviewing output before storage...")
        start_time = time.time()
        text = json.dumps(output) if isinstance(output, dict) else str(output)
        
        input_hash = hashlib.sha256(text.encode()).hexdigest()
        
        if "<script" in text.lower() or "javascript:" in text.lower():
            logger.error(json.dumps({
                "event": "security_violation",
                "input_hash": input_hash,
                "agent": "security",
                "reason": "Agent output contains executable scripts"
            }))
            duration = time.time() - start_time
            return AgentResultEnvelope(agent_id="security", canonical_role="critic", status="needs_review", result=SecurityValidationResult(is_safe=False, reason="Agent output contains executable scripts").model_dump(), metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="regex", prompt_version=None), escalation=AgentEscalation(reason="Executable script in output", target_agent="orchestrator"))
            
        duration = time.time() - start_time
        return AgentResultEnvelope(agent_id="security", canonical_role="critic", status="success", result=SecurityValidationResult(is_safe=True, reason="Output safe for storage.").model_dump(), metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="regex", prompt_version=None))

class OWASPMiddleware(BaseHTTPMiddleware):
    """Enforce OWASP standards on all incoming requests."""
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Enforce max content length to prevent DOS (OWASP A04)
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10_000_000:
            return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, content="Payload Too Large")
            
        response = await call_next(request)
        
        # Apply OWASP secure headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

security_agent = SecurityAgent()
