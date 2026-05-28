# DEV ONLY
import asyncio
from sqlalchemy import text
from ..db import _get_engine
from ..logging_config import get_logger

logger = get_logger(__name__)

async def clear_tables():
    session_maker = _get_engine()
    async with session_maker() as session:
        result = await session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            AND table_name != 'alembic_version';
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            tables_str = ", ".join(f'"{t}"' for t in tables)
            await session.execute(text(f"TRUNCATE {tables_str} CASCADE"))
            logger.info(f"Truncated tables: {tables_str}")
        else:
            logger.info("No tables to truncate.")
            
        await session.commit()

if __name__ == "__main__":
    import os
    import sys
    if os.getenv("ENVIRONMENT") == "production" or "supabase" in os.getenv("DATABASE_URL", "").lower():
        logger.error("Cannot run in production or against external DATABASE_URL")
        sys.exit(1)

    asyncio.run(clear_tables())
    logger.info("Cleared all data from PostgreSQL.")
