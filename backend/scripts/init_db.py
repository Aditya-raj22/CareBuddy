# backend/scripts/init_db.py
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import logging
from app.db.session import engine, SessionLocal
from app.db.models import Base, Doctor, CareBuddy, UserSession, Conversation, Document

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created database tables")
        
        # Create test doctor if it doesn't exist
        db = SessionLocal()
        try:
            doctor = db.query(Doctor).filter(Doctor.id == 1).first()
            if not doctor:
                doctor = Doctor(
                    id=1,
                    uid="DOC1",
                    name="Test Doctor",
                    email="test@example.com"
                )
                db.add(doctor)
                db.commit()
                logger.info("Created test doctor")
            else:
                logger.info("Test doctor already exists")
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        init_database()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)