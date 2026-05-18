from ...logging_config import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)

class SecurityValidationResult(BaseModel):
    is_safe: bool
    reason: str

class SecurityAgent:
    """Validates scraped data and inputs for prompt injection and XSS."""

    def __init__(self):
        pass

    async def sanitize_input(self, text: str) -> str:
        """Strip executable scripts and unsafe HTML tags from input text."""
        logger.info("Security Agent sanitizing input...")
        # Stub: normally use bleach or similar OWASP recommended library
        safe_text = text.replace("<script>", "").replace("</script>", "")
        return safe_text

    async def validate_for_injection(self, text: str) -> SecurityValidationResult:
        """Check for prompt injection techniques."""
        logger.info("Security Agent checking for prompt injection...")
        # Stub: simple heuristic check
        if "ignore all previous instructions" in text.lower():
            return SecurityValidationResult(is_safe=False, reason="Detected prompt injection attempt.")
        return SecurityValidationResult(is_safe=True, reason="Input appears safe.")
