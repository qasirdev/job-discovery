import re
import bleach
import json
import hashlib
from typing import Callable, Any
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
from pydantic import BaseModel
from ...logging_config import get_logger

logger = get_logger("security")

class SecurityValidationResult(BaseModel):
    is_safe: bool
    reason: str
    
    model_config = {"extra": "forbid"}

class SecurityAgent:
    """Validates scraped data and inputs for prompt injection, XSS, and exploit attempts."""

    def __init__(self) -> None:
        self.prompt_path = (
            Path(__file__).parent.parent.parent.parent
            / "prompts"
            / "security-agent"
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

    async def validate_for_injection(self, text: str) -> SecurityValidationResult:
        """Check for prompt injection and SQL/command injection patterns."""
        if not text:
            return SecurityValidationResult(is_safe=True, reason="Input is empty.")

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
                return SecurityValidationResult(is_safe=False, reason=f"Detected potential prompt injection attempt: '{trigger}'")

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
                return SecurityValidationResult(is_safe=False, reason="Detected potential SQL injection exploit attempt.")

        return SecurityValidationResult(is_safe=True, reason="Input appears safe.")

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
