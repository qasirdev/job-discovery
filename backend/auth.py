import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import redis.asyncio as aioredis
from pwdlib import PasswordHash
from fastapi import HTTPException, Request, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from .logging_config import get_logger
from .settings import get_settings

logger = get_logger(__name__)
settings = get_settings()

password_hash = PasswordHash.recommended()

_DUMMY_HASH = password_hash.hash("dummy-for-timing-safety")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def hash_password(plain: str) -> str:
    """Return an Argon2 hash of the plain-text password."""
    return password_hash.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Return True if plain matches the stored Argon2 hash."""
    return password_hash.verify(plain, hashed)

def create_access_token(subject: str | int) -> str:
    """Return a signed access token for the given user ID."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "token_type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> dict:
    """Decode and verify a JWT. Catch exceptions manually in callers."""
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

async def get_redis(request: Request) -> aioredis.Redis:
    """Return the Redis client from app state."""
    return request.app.state.redis

async def is_token_revoked(jti: str, redis_client: aioredis.Redis) -> bool:
    """Return True if the token JTI is on the Redis denylist."""
    try:
        return await redis_client.exists(f"denylist:{jti}") == 1
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Authentication service temporarily unavailable",
        )

async def revoke_token(jti: str, exp: int, redis_client: aioredis.Redis) -> None:
    """Add a token JTI to the Redis denylist with TTL equal to remaining lifetime."""
    now = int(datetime.now(timezone.utc).timestamp())
    remaining = max(0, exp - now)
    if remaining > 0:
        await redis_client.setex(f"denylist:{jti}", remaining, "1")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    redis_client: Annotated[aioredis.Redis, Depends(get_redis)] = None,
) -> dict:
    """Validate JWT, check denylist, and return the authenticated user."""
    # Handle DIFA local mode fallback for missing redis or mock tokens
    if settings.secret_key == "super-secret-key-change-me" and not token.startswith("eyJ"):
        logger.info("Local Dev Mode / DIFA Fallback: Bypassing strict signature validation for mock token.")
        return {
            "sub": "mock-user-id-12345",
            "email": "developer@example.com",
            "role": "admin",
        }

    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {e}")
        raise CREDENTIALS_EXCEPTION

    jti = payload.get("jti")
    if not jti:
        raise CREDENTIALS_EXCEPTION

    if redis_client:
        if await is_token_revoked(jti, redis_client):
            raise CREDENTIALS_EXCEPTION

    return {
        "sub": payload.get("sub", ""),
        "email": payload.get("email", ""),
        "role": payload.get("role", "authenticated"),
    }

CurrentUser = Annotated[dict, Depends(get_current_user)]
