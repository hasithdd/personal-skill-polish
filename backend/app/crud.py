"""CRUD operations for the skill tracker."""

from typing import Optional

from sqlalchemy.orm import Session

from backend.app import models, schemas


def get_phases(db: Session, skip: int = 0, limit: int = 100) -> list[models.Phase]:
    """Get all phases."""
    return db.query(models.Phase).order_by(models.Phase.order).offset(skip).limit(limit).all()


def get_phase(db: Session, phase_id: int) -> Optional[models.Phase]:
    """Get a phase by ID."""
    return db.query(models.Phase).filter(models.Phase.id == phase_id).first()


def create_phase(db: Session, phase: schemas.PhaseCreate) -> models.Phase:
    """Create a new phase."""
    db_phase = models.Phase(
        title=phase.title,
        goal=phase.goal,
        progress=phase.progress,
        notes=phase.notes,
        order=phase.order,
        xp=phase.xp,
    )
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)

    # Create topics
    for topic_data in phase.topics:
        db_topic = models.Topic(
            name=topic_data.name,
            phase_id=db_phase.id,
            progress=topic_data.progress,
            notes=topic_data.notes,
            xp=topic_data.xp,
        )
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)

        # Create subtopics
        for subtopic_data in topic_data.subtopics:
            db_subtopic = models.Subtopic(
                name=subtopic_data.name,
                topic_id=db_topic.id,
                completed=subtopic_data.completed,
                notes=subtopic_data.notes,
                xp=subtopic_data.xp,
            )
            db.add(db_subtopic)

        # Create mastery components
        for mastery_data in topic_data.mastery_components:
            db_mastery = models.MasteryComponent(
                name=mastery_data.name,
                topic_id=db_topic.id,
                level=mastery_data.level,
                notes=mastery_data.notes,
            )
            db.add(db_mastery)

    db.commit()
    db.refresh(db_phase)
    return db_phase


def update_phase(db: Session, phase_id: int, phase: schemas.PhaseUpdate) -> Optional[models.Phase]:
    """Update a phase."""
    db_phase = get_phase(db, phase_id)
    if not db_phase:
        return None

    update_data = phase.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_phase, field, value)

    db.commit()
    db.refresh(db_phase)
    return db_phase


def delete_phase(db: Session, phase_id: int) -> bool:
    """Delete a phase."""
    db_phase = get_phase(db, phase_id)
    if not db_phase:
        return False
    db.delete(db_phase)
    db.commit()
    return True


def get_topic(db: Session, topic_id: int) -> Optional[models.Topic]:
    """Get a topic by ID."""
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()


def create_topic(db: Session, phase_id: int, topic: schemas.TopicCreate) -> models.Topic:
    """Create a new topic."""
    db_topic = models.Topic(
        name=topic.name,
        phase_id=phase_id,
        progress=topic.progress,
        notes=topic.notes,
        xp=topic.xp,
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)

    # Create subtopics
    for subtopic_data in topic.subtopics:
        db_subtopic = models.Subtopic(
            name=subtopic_data.name,
            topic_id=db_topic.id,
            completed=subtopic_data.completed,
            notes=subtopic_data.notes,
            xp=subtopic_data.xp,
        )
        db.add(db_subtopic)

    # Create mastery components
    for mastery_data in topic.mastery_components:
        db_mastery = models.MasteryComponent(
            name=mastery_data.name,
            topic_id=db_topic.id,
            level=mastery_data.level,
            notes=mastery_data.notes,
        )
        db.add(db_mastery)

    db.commit()
    db.refresh(db_topic)
    return db_topic


def update_topic(db: Session, topic_id: int, topic: schemas.TopicUpdate) -> Optional[models.Topic]:
    """Update a topic."""
    db_topic = get_topic(db, topic_id)
    if not db_topic:
        return None

    update_data = topic.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_topic, field, value)

    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_topic(db: Session, topic_id: int) -> bool:
    """Delete a topic."""
    db_topic = get_topic(db, topic_id)
    if not db_topic:
        return False
    db.delete(db_topic)
    db.commit()
    return True


def get_subtopic(db: Session, subtopic_id: int) -> Optional[models.Subtopic]:
    """Get a subtopic by ID."""
    return db.query(models.Subtopic).filter(models.Subtopic.id == subtopic_id).first()


def create_subtopic(
    db: Session, topic_id: int, subtopic: schemas.SubtopicCreate
) -> models.Subtopic:
    """Create a new subtopic."""
    db_subtopic = models.Subtopic(
        name=subtopic.name,
        topic_id=topic_id,
        completed=subtopic.completed,
        notes=subtopic.notes,
        xp=subtopic.xp,
    )
    db.add(db_subtopic)
    db.commit()
    db.refresh(db_subtopic)
    return db_subtopic


def update_subtopic(
    db: Session, subtopic_id: int, subtopic: schemas.SubtopicUpdate
) -> Optional[models.Subtopic]:
    """Update a subtopic."""
    db_subtopic = get_subtopic(db, subtopic_id)
    if not db_subtopic:
        return None

    update_data = subtopic.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subtopic, field, value)

    db.commit()
    db.refresh(db_subtopic)
    return db_subtopic


def delete_subtopic(db: Session, subtopic_id: int) -> bool:
    """Delete a subtopic."""
    db_subtopic = get_subtopic(db, subtopic_id)
    if not db_subtopic:
        return False
    db.delete(db_subtopic)
    db.commit()
    return True


def get_mastery_component(db: Session, mastery_id: int) -> Optional[models.MasteryComponent]:
    """Get a mastery component by ID."""
    return (
        db.query(models.MasteryComponent).filter(models.MasteryComponent.id == mastery_id).first()
    )


def create_mastery_component(
    db: Session, topic_id: int, mastery: schemas.MasteryComponentCreate
) -> models.MasteryComponent:
    """Create a new mastery component."""
    db_mastery = models.MasteryComponent(
        name=mastery.name, topic_id=topic_id, level=mastery.level, notes=mastery.notes
    )
    db.add(db_mastery)
    db.commit()
    db.refresh(db_mastery)
    return db_mastery


def update_mastery_component(
    db: Session, mastery_id: int, mastery: schemas.MasteryComponentUpdate
) -> Optional[models.MasteryComponent]:
    """Update a mastery component."""
    db_mastery = get_mastery_component(db, mastery_id)
    if not db_mastery:
        return None

    update_data = mastery.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mastery, field, value)

    db.commit()
    db.refresh(db_mastery)
    return db_mastery


def delete_mastery_component(db: Session, mastery_id: int) -> bool:
    """Delete a mastery component."""
    db_mastery = get_mastery_component(db, mastery_id)
    if not db_mastery:
        return False
    db.delete(db_mastery)
    db.commit()
    return True


def get_progress_stats(db: Session) -> schemas.ProgressStats:
    """Get overall progress statistics."""
    phases = get_phases(db)
    total_phases = len(phases)
    completed_phases = sum(1 for p in phases if p.progress >= 100.0)
    total_progress = sum(p.progress for p in phases) / total_phases if total_phases > 0 else 0.0
    total_xp = sum(p.xp for p in phases)

    phases_progress = [
        {
            "id": p.id,
            "title": p.title,
            "progress": p.progress,
            "xp": p.xp,
            "order": p.order,
        }
        for p in phases
    ]

    return schemas.ProgressStats(
        total_phases=total_phases,
        completed_phases=completed_phases,
        total_progress=total_progress,
        total_xp=total_xp,
        phases_progress=phases_progress,
    )
