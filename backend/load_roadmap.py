"""Script to load roadmap data into the database."""

import json
import sys
from pathlib import Path

from backend.app import crud, schemas
from backend.app.database import Base, SessionLocal, engine

# Create tables
Base.metadata.create_all(bind=engine)


def load_roadmap(roadmap_file: str) -> None:
    """Load roadmap data from JSON file into database."""
    # Parse roadmap file
    with open(roadmap_file) as f:
        data = json.load(f)

    # Create database session
    db = SessionLocal()

    try:
        # Check if database already has data
        existing_phases = crud.get_phases(db)
        if existing_phases:
            response = input("Database already contains phases. Overwrite? (y/n): ")
            if response.lower() != "y":
                print("Cancelled.")
                return

            # Delete existing phases
            for phase in existing_phases:
                crud.delete_phase(db, phase.id)

        # Load phases
        for phase_data in data.get("phases", []):
            phase_create = schemas.PhaseCreate(**phase_data)
            created_phase = crud.create_phase(db, phase_create)
            print(f"✓ Created phase {created_phase.order}: {created_phase.title}")

        print(f"\n✓ Successfully loaded {len(data.get('phases', []))} phases!")

    except Exception as e:
        print(f"✗ Error loading roadmap: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_roadmap.py <roadmap_file.json>")
        sys.exit(1)

    roadmap_path = sys.argv[1]
    if not Path(roadmap_path).exists():
        print(f"Error: File '{roadmap_path}' not found")
        sys.exit(1)

    load_roadmap(roadmap_path)
