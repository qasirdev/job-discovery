#!/usr/bin/env python3
"""
Factor XII: Admin processes.
This script seeds initial search keywords for scrapers.
"""
from backend.logging_config import get_logger
from backend.filters import INCLUDED_KEYWORDS, EXCLUDED_KEYWORDS

logger = get_logger("admin.seed_keywords")

def run():
    """Seed keywords logic."""
    logger.info("Seeding keyword definitions to database...")
    
    logger.info("Included Keywords to seed:")
    for kw in INCLUDED_KEYWORDS:
        logger.info(f"  -> {kw}")
        
    logger.info("Excluded Keywords to seed:")
    for kw in EXCLUDED_KEYWORDS:
        logger.info(f"  -> {kw}")
        
    # Note for future expansion: If a dynamic DB table for keywords is established,
    # we would perform asynchronous bulk UPSERTs here:
    # Example:
    # async with AsyncSessionLocal() as db:
    #     await db.execute(insert(DBKeyword).values([...]).on_conflict_do_nothing())
    
    logger.info("Seeding complete.")

if __name__ == "__main__":
    run()
