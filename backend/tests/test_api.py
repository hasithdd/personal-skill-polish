"""Tests for the FastAPI application."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_read_root(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_phase(client):
    """Test creating a phase."""
    phase_data = {
        "title": "Test Phase",
        "goal": "Test goal",
        "progress": 0.0,
        "notes": "Test notes",
        "order": 1,
        "xp": 0,
        "topics": [],
    }
    response = client.post("/api/phases", json=phase_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Phase"
    assert data["goal"] == "Test goal"
    assert "id" in data


def test_list_phases(client):
    """Test listing phases."""
    # Create a phase
    phase_data = {
        "title": "Test Phase",
        "goal": "Test goal",
        "progress": 0.0,
        "notes": "Test notes",
        "order": 1,
        "xp": 0,
        "topics": [],
    }
    client.post("/api/phases", json=phase_data)

    # List phases
    response = client.get("/api/phases")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Phase"


def test_get_phase(client):
    """Test getting a specific phase."""
    # Create a phase
    phase_data = {
        "title": "Test Phase",
        "goal": "Test goal",
        "progress": 0.0,
        "notes": "Test notes",
        "order": 1,
        "xp": 0,
        "topics": [],
    }
    create_response = client.post("/api/phases", json=phase_data)
    phase_id = create_response.json()["id"]

    # Get the phase
    response = client.get(f"/api/phases/{phase_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Phase"


def test_update_phase(client):
    """Test updating a phase."""
    # Create a phase
    phase_data = {
        "title": "Test Phase",
        "goal": "Test goal",
        "progress": 0.0,
        "notes": "Test notes",
        "order": 1,
        "xp": 0,
        "topics": [],
    }
    create_response = client.post("/api/phases", json=phase_data)
    phase_id = create_response.json()["id"]

    # Update the phase
    update_data = {"progress": 50.0, "xp": 100}
    response = client.patch(f"/api/phases/{phase_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["progress"] == 50.0
    assert data["xp"] == 100


def test_delete_phase(client):
    """Test deleting a phase."""
    # Create a phase
    phase_data = {
        "title": "Test Phase",
        "goal": "Test goal",
        "progress": 0.0,
        "notes": "Test notes",
        "order": 1,
        "xp": 0,
        "topics": [],
    }
    create_response = client.post("/api/phases", json=phase_data)
    phase_id = create_response.json()["id"]

    # Delete the phase
    response = client.delete(f"/api/phases/{phase_id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/phases/{phase_id}")
    assert response.status_code == 404


def test_get_stats(client):
    """Test getting progress stats."""
    # Create two phases
    phase_data_1 = {
        "title": "Phase 1",
        "goal": "Goal 1",
        "progress": 50.0,
        "notes": "",
        "order": 1,
        "xp": 100,
        "topics": [],
    }
    phase_data_2 = {
        "title": "Phase 2",
        "goal": "Goal 2",
        "progress": 100.0,
        "notes": "",
        "order": 2,
        "xp": 200,
        "topics": [],
    }
    client.post("/api/phases", json=phase_data_1)
    client.post("/api/phases", json=phase_data_2)

    # Get stats
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_phases"] == 2
    assert data["completed_phases"] == 1
    assert data["total_xp"] == 300
