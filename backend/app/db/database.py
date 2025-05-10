# backend/app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import os

logger = logging.getLogger(__name__)

# Create database URL
DATABASE_URL = "sqlite:///carebuddy.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database initialization
def init_db():
    from app.db.models import Doctor, CareBuddy, UserSession, Conversation, Document
    logger.info("Creating database tables...")
    
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    # Create test doctor
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
    except Exception as e:
        logger.error(f"Error creating test doctor: {e}")
        db.rollback()
        raise
    finally:
        db.close()