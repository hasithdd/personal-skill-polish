"""FastAPI main application."""


from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.database import Base, engine, get_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Skill Polish Tracker",
    description="API for tracking AI/ML System Design Roadmap progress",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict:
    """Root endpoint."""
    return {"message": "Personal Skill Polish Tracker API", "version": "0.1.0"}


# Phase endpoints
@app.get("/api/phases", response_model=list[schemas.Phase])
def list_phases(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Phase]:
    """List all phases."""
    phases = crud.get_phases(db, skip=skip, limit=limit)
    return phases


@app.get("/api/phases/{phase_id}", response_model=schemas.Phase)
def get_phase(phase_id: int, db: Session = Depends(get_db)) -> schemas.Phase:
    """Get a specific phase."""
    phase = crud.get_phase(db, phase_id=phase_id)
    if phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    return phase


@app.post("/api/phases", response_model=schemas.Phase, status_code=201)
def create_phase(phase: schemas.PhaseCreate, db: Session = Depends(get_db)) -> schemas.Phase:
    """Create a new phase."""
    return crud.create_phase(db=db, phase=phase)


@app.patch("/api/phases/{phase_id}", response_model=schemas.Phase)
def update_phase(
    phase_id: int, phase: schemas.PhaseUpdate, db: Session = Depends(get_db)
) -> schemas.Phase:
    """Update a phase."""
    updated_phase = crud.update_phase(db=db, phase_id=phase_id, phase=phase)
    if updated_phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    return updated_phase


@app.delete("/api/phases/{phase_id}", status_code=204)
def delete_phase(phase_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a phase."""
    success = crud.delete_phase(db=db, phase_id=phase_id)
    if not success:
        raise HTTPException(status_code=404, detail="Phase not found")


# Topic endpoints
@app.get("/api/topics/{topic_id}", response_model=schemas.Topic)
def get_topic(topic_id: int, db: Session = Depends(get_db)) -> schemas.Topic:
    """Get a specific topic."""
    topic = crud.get_topic(db, topic_id=topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@app.post("/api/phases/{phase_id}/topics", response_model=schemas.Topic, status_code=201)
def create_topic(
    phase_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)
) -> schemas.Topic:
    """Create a new topic."""
    phase = crud.get_phase(db, phase_id=phase_id)
    if phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    return crud.create_topic(db=db, phase_id=phase_id, topic=topic)


@app.patch("/api/topics/{topic_id}", response_model=schemas.Topic)
def update_topic(
    topic_id: int, topic: schemas.TopicUpdate, db: Session = Depends(get_db)
) -> schemas.Topic:
    """Update a topic."""
    updated_topic = crud.update_topic(db=db, topic_id=topic_id, topic=topic)
    if updated_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return updated_topic


@app.delete("/api/topics/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a topic."""
    success = crud.delete_topic(db=db, topic_id=topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")


# Subtopic endpoints
@app.get("/api/subtopics/{subtopic_id}", response_model=schemas.Subtopic)
def get_subtopic(subtopic_id: int, db: Session = Depends(get_db)) -> schemas.Subtopic:
    """Get a specific subtopic."""
    subtopic = crud.get_subtopic(db, subtopic_id=subtopic_id)
    if subtopic is None:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic


@app.post("/api/topics/{topic_id}/subtopics", response_model=schemas.Subtopic, status_code=201)
def create_subtopic(
    topic_id: int, subtopic: schemas.SubtopicCreate, db: Session = Depends(get_db)
) -> schemas.Subtopic:
    """Create a new subtopic."""
    topic = crud.get_topic(db, topic_id=topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return crud.create_subtopic(db=db, topic_id=topic_id, subtopic=subtopic)


@app.patch("/api/subtopics/{subtopic_id}", response_model=schemas.Subtopic)
def update_subtopic(
    subtopic_id: int, subtopic: schemas.SubtopicUpdate, db: Session = Depends(get_db)
) -> schemas.Subtopic:
    """Update a subtopic."""
    updated_subtopic = crud.update_subtopic(db=db, subtopic_id=subtopic_id, subtopic=subtopic)
    if updated_subtopic is None:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return updated_subtopic


@app.delete("/api/subtopics/{subtopic_id}", status_code=204)
def delete_subtopic(subtopic_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a subtopic."""
    success = crud.delete_subtopic(db=db, subtopic_id=subtopic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subtopic not found")


# Mastery component endpoints
@app.get("/api/mastery/{mastery_id}", response_model=schemas.MasteryComponent)
def get_mastery_component(
    mastery_id: int, db: Session = Depends(get_db)
) -> schemas.MasteryComponent:
    """Get a specific mastery component."""
    mastery = crud.get_mastery_component(db, mastery_id=mastery_id)
    if mastery is None:
        raise HTTPException(status_code=404, detail="Mastery component not found")
    return mastery


@app.post(
    "/api/topics/{topic_id}/mastery", response_model=schemas.MasteryComponent, status_code=201
)
def create_mastery_component(
    topic_id: int, mastery: schemas.MasteryComponentCreate, db: Session = Depends(get_db)
) -> schemas.MasteryComponent:
    """Create a new mastery component."""
    topic = crud.get_topic(db, topic_id=topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return crud.create_mastery_component(db=db, topic_id=topic_id, mastery=mastery)


@app.patch("/api/mastery/{mastery_id}", response_model=schemas.MasteryComponent)
def update_mastery_component(
    mastery_id: int, mastery: schemas.MasteryComponentUpdate, db: Session = Depends(get_db)
) -> schemas.MasteryComponent:
    """Update a mastery component."""
    updated_mastery = crud.update_mastery_component(db=db, mastery_id=mastery_id, mastery=mastery)
    if updated_mastery is None:
        raise HTTPException(status_code=404, detail="Mastery component not found")
    return updated_mastery


@app.delete("/api/mastery/{mastery_id}", status_code=204)
def delete_mastery_component(mastery_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a mastery component."""
    success = crud.delete_mastery_component(db=db, mastery_id=mastery_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mastery component not found")


# Progress stats endpoint
@app.get("/api/stats", response_model=schemas.ProgressStats)
def get_stats(db: Session = Depends(get_db)) -> schemas.ProgressStats:
    """Get progress statistics."""
    return crud.get_progress_stats(db=db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
