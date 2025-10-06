"""
FastAPI application for Personal Skill Tracker
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

from backend.app.db import get_db, init_db
from backend.app import models, schemas

app = FastAPI(
    title="Personal Skill Tracker API",
    description="API for tracking progress through AI/ML System Design Roadmap",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


# Phase Endpoints
@app.get("/api/phases", response_model=List[schemas.Phase])
def get_phases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all phases"""
    phases = db.query(models.Phase).order_by(models.Phase.order).offset(skip).limit(limit).all()
    return phases


@app.get("/api/phases/{phase_id}", response_model=schemas.Phase)
def get_phase(phase_id: int, db: Session = Depends(get_db)):
    """Get a specific phase"""
    phase = db.query(models.Phase).filter(models.Phase.id == phase_id).first()
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    return phase


@app.post("/api/phases", response_model=schemas.Phase)
def create_phase(phase: schemas.PhaseCreate, db: Session = Depends(get_db)):
    """Create a new phase"""
    db_phase = models.Phase(**phase.dict())
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase


@app.put("/api/phases/{phase_id}", response_model=schemas.Phase)
def update_phase(phase_id: int, phase: schemas.PhaseUpdate, db: Session = Depends(get_db)):
    """Update a phase"""
    db_phase = db.query(models.Phase).filter(models.Phase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")

    for key, value in phase.dict(exclude_unset=True).items():
        setattr(db_phase, key, value)

    db.commit()
    db.refresh(db_phase)
    return db_phase


@app.delete("/api/phases/{phase_id}")
def delete_phase(phase_id: int, db: Session = Depends(get_db)):
    """Delete a phase"""
    db_phase = db.query(models.Phase).filter(models.Phase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")

    db.delete(db_phase)
    db.commit()
    return {"message": "Phase deleted successfully"}


# Topic Endpoints
@app.get("/api/topics", response_model=List[schemas.Topic])
def get_topics(
    phase_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all topics, optionally filtered by phase"""
    query = db.query(models.Topic)
    if phase_id:
        query = query.filter(models.Topic.phase_id == phase_id)
    topics = query.order_by(models.Topic.order).offset(skip).limit(limit).all()
    return topics


@app.get("/api/topics/{topic_id}", response_model=schemas.Topic)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get a specific topic"""
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@app.post("/api/topics", response_model=schemas.Topic)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    """Create a new topic"""
    db_topic = models.Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


@app.put("/api/topics/{topic_id}", response_model=schemas.Topic)
def update_topic(topic_id: int, topic: schemas.TopicUpdate, db: Session = Depends(get_db)):
    """Update a topic"""
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    for key, value in topic.dict(exclude_unset=True).items():
        setattr(db_topic, key, value)

    db.commit()
    db.refresh(db_topic)
    return db_topic


@app.delete("/api/topics/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """Delete a topic"""
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.delete(db_topic)
    db.commit()
    return {"message": "Topic deleted successfully"}


# Subtopic Endpoints
@app.get("/api/subtopics", response_model=List[schemas.Subtopic])
def get_subtopics(
    topic_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all subtopics, optionally filtered by topic"""
    query = db.query(models.Subtopic)
    if topic_id:
        query = query.filter(models.Subtopic.topic_id == topic_id)
    subtopics = query.order_by(models.Subtopic.order).offset(skip).limit(limit).all()
    return subtopics


@app.get("/api/subtopics/{subtopic_id}", response_model=schemas.Subtopic)
def get_subtopic(subtopic_id: int, db: Session = Depends(get_db)):
    """Get a specific subtopic"""
    subtopic = db.query(models.Subtopic).filter(models.Subtopic.id == subtopic_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic


@app.post("/api/subtopics", response_model=schemas.Subtopic)
def create_subtopic(subtopic: schemas.SubtopicCreate, db: Session = Depends(get_db)):
    """Create a new subtopic"""
    db_subtopic = models.Subtopic(**subtopic.dict())
    db.add(db_subtopic)
    db.commit()
    db.refresh(db_subtopic)
    return db_subtopic


@app.put("/api/subtopics/{subtopic_id}", response_model=schemas.Subtopic)
def update_subtopic(
    subtopic_id: int, subtopic: schemas.SubtopicUpdate, db: Session = Depends(get_db)
):
    """Update a subtopic"""
    db_subtopic = db.query(models.Subtopic).filter(models.Subtopic.id == subtopic_id).first()
    if not db_subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    for key, value in subtopic.dict(exclude_unset=True).items():
        setattr(db_subtopic, key, value)

    db.commit()
    db.refresh(db_subtopic)
    return db_subtopic


@app.delete("/api/subtopics/{subtopic_id}")
def delete_subtopic(subtopic_id: int, db: Session = Depends(get_db)):
    """Delete a subtopic"""
    db_subtopic = db.query(models.Subtopic).filter(models.Subtopic.id == subtopic_id).first()
    if not db_subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    db.delete(db_subtopic)
    db.commit()
    return {"message": "Subtopic deleted successfully"}


# Mastery Component Endpoints
@app.get("/api/mastery-components", response_model=List[schemas.MasteryComponent])
def get_mastery_components(
    subtopic_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all mastery components, optionally filtered by subtopic"""
    query = db.query(models.MasteryComponent)
    if subtopic_id:
        query = query.filter(models.MasteryComponent.subtopic_id == subtopic_id)
    components = query.offset(skip).limit(limit).all()
    return components


@app.get("/api/mastery-components/{component_id}", response_model=schemas.MasteryComponent)
def get_mastery_component(component_id: int, db: Session = Depends(get_db)):
    """Get a specific mastery component"""
    component = (
        db.query(models.MasteryComponent).filter(models.MasteryComponent.id == component_id).first()
    )
    if not component:
        raise HTTPException(status_code=404, detail="Mastery component not found")
    return component


@app.post("/api/mastery-components", response_model=schemas.MasteryComponent)
def create_mastery_component(
    component: schemas.MasteryComponentCreate, db: Session = Depends(get_db)
):
    """Create a new mastery component"""
    db_component = models.MasteryComponent(**component.dict())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component


@app.put("/api/mastery-components/{component_id}", response_model=schemas.MasteryComponent)
def update_mastery_component(
    component_id: int, component: schemas.MasteryComponentUpdate, db: Session = Depends(get_db)
):
    """Update a mastery component"""
    db_component = (
        db.query(models.MasteryComponent).filter(models.MasteryComponent.id == component_id).first()
    )
    if not db_component:
        raise HTTPException(status_code=404, detail="Mastery component not found")

    for key, value in component.dict(exclude_unset=True).items():
        setattr(db_component, key, value)

    db.commit()
    db.refresh(db_component)
    return db_component


@app.delete("/api/mastery-components/{component_id}")
def delete_mastery_component(component_id: int, db: Session = Depends(get_db)):
    """Delete a mastery component"""
    db_component = (
        db.query(models.MasteryComponent).filter(models.MasteryComponent.id == component_id).first()
    )
    if not db_component:
        raise HTTPException(status_code=404, detail="Mastery component not found")

    db.delete(db_component)
    db.commit()
    return {"message": "Mastery component deleted successfully"}


# Progress Endpoints
@app.get("/api/progress", response_model=List[schemas.Progress])
def get_progress(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all progress records"""
    progress = db.query(models.Progress).offset(skip).limit(limit).all()
    return progress


@app.get("/api/progress/{progress_id}", response_model=schemas.Progress)
def get_progress_by_id(progress_id: int, db: Session = Depends(get_db)):
    """Get a specific progress record"""
    progress = db.query(models.Progress).filter(models.Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress


@app.post("/api/progress", response_model=schemas.Progress)
def create_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    """Create a new progress record"""
    db_progress = models.Progress(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


@app.put("/api/progress/{progress_id}", response_model=schemas.Progress)
def update_progress(
    progress_id: int, progress: schemas.ProgressUpdate, db: Session = Depends(get_db)
):
    """Update a progress record"""
    db_progress = db.query(models.Progress).filter(models.Progress.id == progress_id).first()
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    for key, value in progress.dict(exclude_unset=True).items():
        setattr(db_progress, key, value)

    db.commit()
    db.refresh(db_progress)
    return db_progress


@app.delete("/api/progress/{progress_id}")
def delete_progress(progress_id: int, db: Session = Depends(get_db)):
    """Delete a progress record"""
    db_progress = db.query(models.Progress).filter(models.Progress.id == progress_id).first()
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    db.delete(db_progress)
    db.commit()
    return {"message": "Progress deleted successfully"}


# Note Endpoints
@app.get("/api/notes", response_model=List[schemas.Note])
def get_notes(
    progress_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all notes, optionally filtered by progress"""
    query = db.query(models.Note)
    if progress_id:
        query = query.filter(models.Note.progress_id == progress_id)
    notes = query.offset(skip).limit(limit).all()
    return notes


@app.post("/api/notes", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    db_note = models.Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.put("/api/notes/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    """Update a note"""
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note"""
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}


# Achievement Endpoints
@app.get("/api/achievements", response_model=List[schemas.Achievement])
def get_achievements(db: Session = Depends(get_db)):
    """Get all achievements"""
    achievements = db.query(models.Achievement).all()
    return achievements


@app.post("/api/achievements", response_model=schemas.Achievement)
def create_achievement(achievement: schemas.AchievementCreate, db: Session = Depends(get_db)):
    """Create a new achievement"""
    db_achievement = models.Achievement(**achievement.dict())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


# Stats Endpoints
@app.get("/api/stats", response_model=schemas.Stats)
def get_stats(db: Session = Depends(get_db)):
    """Get overall statistics"""
    stats = db.query(models.Stats).first()
    if not stats:
        # Create default stats if not exists
        stats = models.Stats()
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


# Dashboard Endpoint
@app.get("/api/dashboard", response_model=schemas.Dashboard)
def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard data with stats, recent progress, and achievements"""
    stats = db.query(models.Stats).first()
    if not stats:
        stats = models.Stats()
        db.add(stats)
        db.commit()
        db.refresh(stats)

    recent_progress = (
        db.query(models.Progress).order_by(models.Progress.updated_at.desc()).limit(10).all()
    )
    achievements = db.query(models.Achievement).filter(models.Achievement.unlocked == True).all()

    phases = db.query(models.Phase).order_by(models.Phase.order).all()
    phases_summary = []
    for phase in phases:
        total_topics = len(phase.topics)
        completed_topics = sum(
            1 for t in phase.topics if any(p.status == "completed" for p in t.progress)
        )
        phases_summary.append(
            {
                "id": phase.id,
                "name": phase.name,
                "total_topics": total_topics,
                "completed_topics": completed_topics,
                "progress_percentage": (completed_topics / total_topics * 100)
                if total_topics > 0
                else 0,
            }
        )

    return {
        "stats": stats,
        "recent_progress": recent_progress,
        "achievements": achievements,
        "phases_summary": phases_summary,
    }


# Export Endpoint
@app.get("/api/export")
def export_data(db: Session = Depends(get_db)):
    """Export all data as JSON"""
    data = {
        "phases": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "order": p.order,
                "topics": [
                    {
                        "id": t.id,
                        "name": t.name,
                        "description": t.description,
                        "order": t.order,
                        "subtopics": [
                            {
                                "id": s.id,
                                "name": s.name,
                                "description": s.description,
                                "order": s.order,
                            }
                            for s in t.subtopics
                        ],
                    }
                    for t in p.topics
                ],
            }
            for p in db.query(models.Phase).order_by(models.Phase.order).all()
        ],
        "progress": [
            {
                "id": p.id,
                "phase_id": p.phase_id,
                "topic_id": p.topic_id,
                "subtopic_id": p.subtopic_id,
                "mastery_component_id": p.mastery_component_id,
                "status": p.status,
                "completion_percentage": p.completion_percentage,
                "hours_spent": p.hours_spent,
                "last_studied": p.last_studied.isoformat() if p.last_studied else None,
            }
            for p in db.query(models.Progress).all()
        ],
        "stats": {
            "total_points": db.query(models.Stats).first().total_points
            if db.query(models.Stats).first()
            else 0,
            "total_hours": db.query(models.Stats).first().total_hours
            if db.query(models.Stats).first()
            else 0,
        },
    }
    return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
