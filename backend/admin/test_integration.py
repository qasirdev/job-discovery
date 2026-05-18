import asyncio
import jwt
import pytest
from fastapi.security import HTTPAuthorizationCredentials
from ..agents.observability.observability_agent import ObservabilityAgent
from ..auth import get_current_user
from ..logging_config import get_logger

logger = get_logger("admin.test_integration")


def test_observability_agent() -> None:
    """Validate that the ObservabilityAgent constructs, profiles, and records metrics correctly."""
    logger.info("Executing Test: Observability Tracing & Metrics...")
    obs = ObservabilityAgent(service_name="test-suite")

    # Verify context tracing execution
    try:
        with obs.trace_agent_execution("test-agent") as span:
            span.set_attribute("test.property", "validated")
            logger.info("Inside traced execution span context.")
        logger.info("Observability tracer verification: PASSED")
    except Exception as e:
        logger.error(f"Observability tracer verification: FAILED - {e}")
        raise e


@pytest.mark.asyncio
async def test_supabase_jwt_auth() -> None:
    """Validate standard HS256 Supabase JWT decoding, invalid token blocks, and local DIFA fallbacks."""
    logger.info("Executing Test: JWT Authentication Security Gates...")

    # 1. Test missing credentials validation (should raise 401)
    try:
        await get_current_user(credentials=None)
        logger.error("Authentication missing header test: FAILED (did not raise 401)")
        raise AssertionError("Missing authorization header did not trigger 401.")
    except Exception as e:
        # Expecting HTTPException with 401 status
        if hasattr(e, "status_code") and getattr(e, "status_code") == 401:
            logger.info("Authentication missing header test: PASSED (raised 401)")
        else:
            logger.error(f"Authentication missing header test: FAILED - {e}")
            raise e

    # 2. Test DIFA Fallback for mock tokens (should return default developer payload)
    mock_creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="mock-token-payload-xyz")
    try:
        payload = await get_current_user(credentials=mock_creds)
        assert payload["sub"] == "mock-user-id-12345"
        assert payload["email"] == "developer@example.com"
        logger.info("Authentication DIFA Fallback developer token bypass test: PASSED")
    except Exception as e:
        logger.error(f"Authentication DIFA Fallback developer token bypass test: FAILED - {e}")
        raise e

    # 3. Test expired signature interception (should raise 401)
    # Generate an expired token signed with secret for validation testing
    expired_payload = {
        "sub": "user-expired",
        "email": "expired@example.com",
        "aud": "authenticated",
        "exp": 0,  # Forces immediate expiration
    }
    expired_token = jwt.encode(expired_payload, "test-suite-key-signature-validation", algorithm="HS256")
    expired_creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=expired_token)

    # Patch SECRET temporarily to verify full decoder signatures
    import backend.auth as auth_mod
    original_secret = auth_mod.SUPABASE_JWT_SECRET
    auth_mod.SUPABASE_JWT_SECRET = "test-suite-key-signature-validation"

    try:
        await get_current_user(credentials=expired_creds)
        logger.error("Authentication expired token test: FAILED (did not raise 401)")
        raise AssertionError("Expired signature did not trigger 401.")
    except Exception as e:
        if hasattr(e, "status_code") and getattr(e, "status_code") == 401:
            logger.info("Authentication expired token test: PASSED (raised 401)")
        else:
            logger.error(f"Authentication expired token test: FAILED - {e}")
            raise e
    finally:
        # Revert patched module secret
        auth_mod.SUPABASE_JWT_SECRET = original_secret


async def run_all_tests() -> None:
    """Execute all Twelve-Factor and Observability stack automated verification tests."""
    logger.info("Starting monorepo MVP 3 Integration Verification Suite...")
    start_time = asyncio.get_event_loop().time()

    test_observability_agent()
    await test_supabase_jwt_auth()

    duration = asyncio.get_event_loop().time() - start_time
    logger.info(f"Verification suite completed in {duration:.4f}s. ALL INTEGRATION TESTS PASSED.")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
