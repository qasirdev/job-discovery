#!/usr/bin/env python3
"""
Factor XII: Admin processes.
Clears the database for development environments.
"""
import asyncio
from sqlalchemy import delete
from backend.db import AsyncSessionLocal
from backend.models import Job as DBJob
from backend.logging_config import get_logger

logger = get_logger("admin.clear_db")


async def run_async() -> None:
    """Clear the jobs table inside PostgreSQL."""
    logger.warning("Clearing database table 'jobs'...")
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(delete(DBJob))
            await db.commit()
            # rowcount represents number of deleted rows in SQL
            rows_deleted = getattr(result, "rowcount", 0)

            logger.info(f"Database cleared successfully. {rows_deleted} records deleted from 'jobs'.")
    except Exception as e:
        logger.error(f"Failed to clear database: {e}", exc_info=True)


def run() -> None:
    asyncio.run(run_async())


if __name__ == "__main__":
    run()
