# backend/scripts/create_db.py
import logging
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        from app.db.database import init_db
        init_db()
        logger.info("Database initialization complete!")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        sys.exit(1)