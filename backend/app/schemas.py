"""Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MasteryComponentBase(BaseModel):
    """Base schema for mastery component."""

    name: str
    level: int = Field(default=0, ge=0, le=5)
    notes: Optional[str] = None


class MasteryComponentCreate(MasteryComponentBase):
    """Schema for creating a mastery component."""

    pass


class MasteryComponentUpdate(BaseModel):
    """Schema for updating a mastery component."""

    name: Optional[str] = None
    level: Optional[int] = Field(default=None, ge=0, le=5)
    notes: Optional[str] = None


class MasteryComponent(MasteryComponentBase):
    """Schema for mastery component response."""

    id: int
    topic_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubtopicBase(BaseModel):
    """Base schema for subtopic."""

    name: str
    completed: int = Field(default=0, ge=0, le=2)
    notes: Optional[str] = None
    xp: int = 0


class SubtopicCreate(SubtopicBase):
    """Schema for creating a subtopic."""

    pass


class SubtopicUpdate(BaseModel):
    """Schema for updating a subtopic."""

    name: Optional[str] = None
    completed: Optional[int] = Field(default=None, ge=0, le=2)
    notes: Optional[str] = None
    xp: Optional[int] = None


class Subtopic(SubtopicBase):
    """Schema for subtopic response."""

    id: int
    topic_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TopicBase(BaseModel):
    """Base schema for topic."""

    name: str
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    notes: Optional[str] = None
    xp: int = 0


class TopicCreate(TopicBase):
    """Schema for creating a topic."""

    subtopics: list[SubtopicCreate] = []
    mastery_components: list[MasteryComponentCreate] = []


class TopicUpdate(BaseModel):
    """Schema for updating a topic."""

    name: Optional[str] = None
    progress: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    notes: Optional[str] = None
    xp: Optional[int] = None


class Topic(TopicBase):
    """Schema for topic response."""

    id: int
    phase_id: int
    subtopics: list[Subtopic] = []
    mastery_components: list[MasteryComponent] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhaseBase(BaseModel):
    """Base schema for phase."""

    title: str
    goal: str
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    notes: Optional[str] = None
    order: int
    xp: int = 0


class PhaseCreate(PhaseBase):
    """Schema for creating a phase."""

    topics: list[TopicCreate] = []


class PhaseUpdate(BaseModel):
    """Schema for updating a phase."""

    title: Optional[str] = None
    goal: Optional[str] = None
    progress: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    notes: Optional[str] = None
    order: Optional[int] = None
    xp: Optional[int] = None


class Phase(PhaseBase):
    """Schema for phase response."""

    id: int
    topics: list[Topic] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressStats(BaseModel):
    """Schema for progress statistics."""

    total_phases: int
    completed_phases: int
    total_progress: float
    total_xp: int
    phases_progress: list[dict]
