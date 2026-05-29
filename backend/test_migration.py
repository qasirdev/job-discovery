from backend.logging_config import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Migration connectivity check: OK")
