import logging
from ..settings import settings
from ..logging_config import get_logger
from ..filters import DEFAULT_KEYWORDS

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info(f"Seeding {len(DEFAULT_KEYWORDS)} keywords:")
    for kw in DEFAULT_KEYWORDS:
        print(kw)
    # Stub for future Supabase insert
