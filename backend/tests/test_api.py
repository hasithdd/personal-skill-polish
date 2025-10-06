"""
Unit tests for the Personal Skill Tracker API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.db import get_db
from backend.app.models import Base

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_root():
    """Test that the API is accessible"""
    response = client.get("/api/phases")
    assert response.status_code == 200


def test_create_phase():
    """Test creating a new phase"""
    response = client.post(
        "/api/phases", json={"name": "Test Phase", "description": "Test Description", "order": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Phase"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_get_phases():
    """Test getting all phases"""
    # Create a phase first
    client.post(
        "/api/phases", json={"name": "Test Phase", "description": "Test Description", "order": 1}
    )

    response = client.get("/api/phases")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_phase_by_id():
    """Test getting a specific phase"""
    # Create a phase
    create_response = client.post(
        "/api/phases", json={"name": "Test Phase", "description": "Test Description", "order": 1}
    )
    phase_id = create_response.json()["id"]

    # Get the phase
    response = client.get(f"/api/phases/{phase_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == phase_id
    assert data["name"] == "Test Phase"


def test_update_phase():
    """Test updating a phase"""
    # Create a phase
    create_response = client.post(
        "/api/phases", json={"name": "Test Phase", "description": "Test Description", "order": 1}
    )
    phase_id = create_response.json()["id"]

    # Update the phase
    response = client.put(f"/api/phases/{phase_id}", json={"name": "Updated Phase"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Phase"
    assert data["description"] == "Test Description"  # Should remain unchanged


def test_delete_phase():
    """Test deleting a phase"""
    # Create a phase
    create_response = client.post(
        "/api/phases", json={"name": "Test Phase", "description": "Test Description", "order": 1}
    )
    phase_id = create_response.json()["id"]

    # Delete the phase
    response = client.delete(f"/api/phases/{phase_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/api/phases/{phase_id}")
    assert get_response.status_code == 404


def test_create_topic():
    """Test creating a topic"""
    # Create a phase first
    phase_response = client.post(
        "/api/phases", json={"name": "Test Phase", "description": "Test Description", "order": 1}
    )
    phase_id = phase_response.json()["id"]

    # Create a topic
    response = client.post(
        "/api/topics",
        json={
            "phase_id": phase_id,
            "name": "Test Topic",
            "description": "Test Topic Description",
            "order": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Topic"
    assert data["phase_id"] == phase_id


def test_get_stats():
    """Test getting stats"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_points" in data
    assert "total_hours" in data
    assert "current_streak" in data


def test_get_dashboard():
    """Test getting dashboard data"""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "stats" in data
    assert "recent_progress" in data
    assert "achievements" in data
    assert "phases_summary" in data


def test_export_data():
    """Test exporting data"""
    response = client.get("/api/export")
    assert response.status_code == 200
    data = response.json()
    assert "phases" in data
    assert "progress" in data
    assert "stats" in data
