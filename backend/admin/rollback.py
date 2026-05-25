import subprocess
from ..logging_config import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Running database rollback (Alembic downgrade -1)...")
    try:
        # Run alembic downgrade -1
        result = subprocess.run(["alembic", "downgrade", "-1"], check=True, capture_output=True, text=True)
        logger.info("Rollback successful.")
        logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Rollback failed: {e.stderr}")
        exit(1)
