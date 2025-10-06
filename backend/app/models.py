"""SQLAlchemy models for skill tracking."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Phase(Base):
    """Phase model representing a learning phase."""

    __tablename__ = "phases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    progress = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    xp = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    topics = relationship("Topic", back_populates="phase", cascade="all, delete-orphan")


class Topic(Base):
    """Topic model representing a topic within a phase."""

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phase_id = Column(Integer, ForeignKey("phases.id"), nullable=False)
    progress = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    xp = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    phase = relationship("Phase", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    mastery_components = relationship(
        "MasteryComponent", back_populates="topic", cascade="all, delete-orphan"
    )


class Subtopic(Base):
    """Subtopic model representing a subtopic within a topic."""

    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    completed = Column(Integer, default=0)  # 0 = not started, 1 = in progress, 2 = completed
    notes = Column(Text, nullable=True)
    xp = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    topic = relationship("Topic", back_populates="subtopics")


class MasteryComponent(Base):
    """Mastery component model for tracking mastery skills."""

    __tablename__ = "mastery_components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    level = Column(Integer, default=0)  # 0-5 scale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    topic = relationship("Topic", back_populates="mastery_components")
