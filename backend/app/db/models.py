# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    uid = Column(String(4), unique=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    care_buddies = relationship("CareBuddy", back_populates="doctor")

class CareBuddy(Base):
    __tablename__ = 'care_buddies'
    id = Column(Integer, primary_key=True)
    bid = Column(String(6), unique=True)
    name = Column(String(100))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    doctor = relationship("Doctor", back_populates="care_buddies")
    conversations = relationship("Conversation", back_populates="care_buddy")
    documents = relationship("Document", back_populates="care_buddy")

class UserSession(Base):
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20))
    buddy_id = Column(Integer, ForeignKey('care_buddies.id'))
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_active = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    conversations = relationship("Conversation", back_populates="user_session")
    care_buddy = relationship("CareBuddy")

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    buddy_id = Column(Integer, ForeignKey('care_buddies.id'))
    user_session_id = Column(Integer, ForeignKey('user_sessions.id'))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    query = Column(Text)
    response = Column(Text)
    helpful = Column(Boolean, nullable=True)
    user_session = relationship("UserSession", back_populates="conversations")
    care_buddy = relationship("CareBuddy", back_populates="conversations")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    buddy_id = Column(Integer, ForeignKey('care_buddies.id'))
    filename = Column(String(255))
    content = Column(Text)
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    care_buddy = relationship("CareBuddy", back_populates="documents")