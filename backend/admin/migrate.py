import subprocess
from ..logging_config import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Running database migration (Alembic upgrade head)...")
    try:
        # Run alembic upgrade head
        result = subprocess.run(["alembic", "upgrade", "head"], check=True, capture_output=True, text=True)
        logger.info("Migration successful.")
        logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e.stderr}")
        exit(1)
