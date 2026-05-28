import os
import yaml
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..logging_config import get_logger
from ..db import _get_engine
from ..settings import get_settings
from ..models import UserProfile
from ..services.filters import DEFAULT_KEYWORDS

logger = get_logger(__name__)

async def seed_keywords():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "relevance_profile.yaml")
    
    target_roles = ["senior", "lead", "principal", "architect"]
    preferred_stack = ["python", "fastapi", "next.js", "typescript", "azure", "aws", "llm", "ai"]
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    target_roles = data.get("seniority_keywords", target_roles)
                    preferred_stack = data.get("stack_keywords", preferred_stack)
        except Exception as e:
            logger.warning(f"Failed to load yaml, using defaults: {e}")
            
    user_id = get_settings().single_user_id
    session_maker = _get_engine()
    
    async with session_maker() as session:
        result = await session.execute(select(UserProfile).where(UserProfile.id == user_id))
        profile = result.scalar_one_or_none()
        
        if not profile:
            logger.info("Creating default UserProfile with seeded keywords")
            profile = UserProfile(
                id=user_id,
                full_name="Default User",
                email="default@example.com",
                target_role="Senior AI Engineer",
                target_location="London",
                years_experience=8,
                target_roles=target_roles,
                preferred_stack=preferred_stack
            )
            session.add(profile)
        else:
            logger.info("Updating existing UserProfile with seeded keywords")
            profile.target_roles = target_roles
            profile.preferred_stack = preferred_stack
            
        await session.commit()
        logger.info(f"Successfully seeded {len(target_roles)} target roles and {len(preferred_stack)} stack keywords for user {user_id}")

if __name__ == "__main__":
    asyncio.run(seed_keywords())
