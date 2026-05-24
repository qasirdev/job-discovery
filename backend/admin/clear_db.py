# DEV ONLY
import os
import sys
from ..fake_db import clear_jobs
from ..logging_config import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    if os.getenv("DATABASE_URL"):
        logger.error("Cannot run in production")
        sys.exit(1)

    clear_jobs()
    logger.info("Cleared jobs from fake_db.")
