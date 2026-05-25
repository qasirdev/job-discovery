# DEV ONLY
import asyncio
from sqlalchemy import text
from ..db import _get_engine
from ..logging_config import get_logger

logger = get_logger(__name__)

async def clear_tables():
    session_maker = _get_engine()
    async with session_maker() as session:
        # Cascade truncate to clear all tables
        await session.execute(text("TRUNCATE TABLE jobs, recruiter, applications, cv, cover_letter, scrape_runs, interview_prep, audit_log CASCADE"))
        await session.commit()

if __name__ == "__main__":
    import os
    import sys
    if os.getenv("ENVIRONMENT") == "production" or "supabase" in os.getenv("DATABASE_URL", "").lower():
        logger.error("Cannot run in production or against external DATABASE_URL")
        sys.exit(1)

    asyncio.run(clear_tables())
    logger.info("Cleared all data from PostgreSQL.")
