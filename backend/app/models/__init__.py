"""
SQLAlchemy database models for the Personal Skill Tracker
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Phase(Base):
    """Represents a major phase in the learning roadmap"""

    __tablename__ = "phases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topics = relationship("Topic", back_populates="phase", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="phase", cascade="all, delete-orphan")


class Topic(Base):
    """Represents a topic within a phase"""

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    phase_id = Column(Integer, ForeignKey("phases.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    phase = relationship("Phase", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="topic", cascade="all, delete-orphan")


class Subtopic(Base):
    """Represents a subtopic within a topic"""

    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topic = relationship("Topic", back_populates="subtopics")
    mastery_components = relationship(
        "MasteryComponent", back_populates="subtopic", cascade="all, delete-orphan"
    )
    progress = relationship("Progress", back_populates="subtopic", cascade="all, delete-orphan")


class MasteryComponent(Base):
    """Represents components required to master a subtopic"""

    __tablename__ = "mastery_components"

    id = Column(Integer, primary_key=True, index=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    component_type = Column(String(50))  # e.g., 'theory', 'practice', 'project'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subtopic = relationship("Subtopic", back_populates="mastery_components")
    progress = relationship(
        "Progress", back_populates="mastery_component", cascade="all, delete-orphan"
    )


class Progress(Base):
    """Tracks progress for phases, topics, subtopics, or mastery components"""

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    phase_id = Column(Integer, ForeignKey("phases.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=True)
    mastery_component_id = Column(Integer, ForeignKey("mastery_components.id"), nullable=True)

    status = Column(String(50), default="not_started")  # not_started, in_progress, completed
    completion_percentage = Column(Float, default=0.0)
    hours_spent = Column(Float, default=0.0)
    last_studied = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    phase = relationship("Phase", back_populates="progress")
    topic = relationship("Topic", back_populates="progress")
    subtopic = relationship("Subtopic", back_populates="progress")
    mastery_component = relationship("MasteryComponent", back_populates="progress")
    notes = relationship("Note", back_populates="progress", cascade="all, delete-orphan")


class Note(Base):
    """Notes associated with progress tracking"""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("progress.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    progress = relationship("Progress", back_populates="notes")


class Achievement(Base):
    """Gamification: Achievements/badges earned"""

    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    icon = Column(String(100))
    points = Column(Integer, default=0)
    requirement = Column(Text)  # Description of how to earn this
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class Stats(Base):
    """Overall statistics and gamification metrics"""

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_hours = Column(Float, default=0.0)
    phases_completed = Column(Integer, default=0)
    topics_completed = Column(Integer, default=0)
    subtopics_completed = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
