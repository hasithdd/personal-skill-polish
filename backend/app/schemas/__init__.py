"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Phase Schemas
class PhaseBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    order: int


class PhaseCreate(PhaseBase):
    pass


class PhaseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = None


class Phase(PhaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Topic Schemas
class TopicBase(BaseModel):
    phase_id: int
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    order: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = None


class Topic(TopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Subtopic Schemas
class SubtopicBase(BaseModel):
    topic_id: int
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    order: int


class SubtopicCreate(SubtopicBase):
    pass


class SubtopicUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = None


class Subtopic(SubtopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Mastery Component Schemas
class MasteryComponentBase(BaseModel):
    subtopic_id: int
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    component_type: Optional[str] = Field(None, max_length=50)


class MasteryComponentCreate(MasteryComponentBase):
    pass


class MasteryComponentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    component_type: Optional[str] = Field(None, max_length=50)


class MasteryComponent(MasteryComponentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Progress Schemas
class ProgressBase(BaseModel):
    phase_id: Optional[int] = None
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    mastery_component_id: Optional[int] = None
    status: str = Field(default="not_started", max_length=50)
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    hours_spent: float = Field(default=0.0, ge=0.0)
    last_studied: Optional[datetime] = None


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)
    completion_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    hours_spent: Optional[float] = Field(None, ge=0.0)
    last_studied: Optional[datetime] = None


class Progress(ProgressBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Note Schemas
class NoteBase(BaseModel):
    progress_id: int
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    content: str


class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Achievement Schemas
class AchievementBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    points: int = Field(default=0, ge=0)
    requirement: Optional[str] = None


class AchievementCreate(AchievementBase):
    pass


class Achievement(AchievementBase):
    id: int
    unlocked: bool
    unlocked_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Stats Schemas
class Stats(BaseModel):
    id: int
    total_points: int
    current_streak: int
    longest_streak: int
    total_hours: float
    phases_completed: int
    topics_completed: int
    subtopics_completed: int
    last_updated: datetime

    class Config:
        from_attributes = True


# Dashboard Schema
class Dashboard(BaseModel):
    stats: Stats
    recent_progress: List[Progress]
    achievements: List[Achievement]
    phases_summary: List[dict]
