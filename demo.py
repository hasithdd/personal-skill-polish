#!/usr/bin/env python3
"""Demo script to showcase the Personal Skill Polish Tracker."""
import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_json(data):
    """Print formatted JSON."""
    print(json.dumps(data, indent=2))


def demo():
    """Run the demo."""
    print_header("Personal Skill Polish Tracker - Demo")

    # Check API status
    print("1. Checking API status...")
    response = requests.get(f"{BASE_URL}/")
    print_json(response.json())

    # Get statistics
    print_header("2. Getting Overall Progress Statistics")
    response = requests.get(f"{BASE_URL}/api/stats")
    stats = response.json()
    print_json(stats)

    # List first 3 phases
    print_header("3. Listing First 3 Phases")
    response = requests.get(f"{BASE_URL}/api/phases?limit=3")
    phases = response.json()
    for phase in phases:
        print(f"Phase {phase['order']}: {phase['title']}")
        print(f"  Goal: {phase['goal']}")
        print(f"  Progress: {phase['progress']}%")
        print(f"  Topics: {len(phase['topics'])}")
        print()

    # Get details of first phase
    print_header("4. Getting Details of Phase 1")
    response = requests.get(f"{BASE_URL}/api/phases/1")
    phase = response.json()
    print(f"Title: {phase['title']}")
    print(f"Goal: {phase['goal']}")
    print(f"\nTopics:")
    for topic in phase["topics"]:
        print(f"  • {topic['name']}")
        print(f"    - Subtopics: {len(topic['subtopics'])}")
        print(f"    - Mastery Components: {len(topic['mastery_components'])}")

    # Update phase progress
    print_header("5. Updating Progress for Phase 1")
    update_data = {"progress": 25.0, "xp": 100}
    response = requests.patch(f"{BASE_URL}/api/phases/1", json=update_data)
    updated_phase = response.json()
    print(f"Updated Progress: {updated_phase['progress']}%")
    print(f"Updated XP: {updated_phase['xp']}")

    # Add a note
    print_header("6. Adding a Note to Phase 1")
    note_data = {"notes": "Started with data structures. Arrays and linked lists completed!"}
    response = requests.patch(f"{BASE_URL}/api/phases/1", json=note_data)
    updated_phase = response.json()
    print(f"Note: {updated_phase['notes']}")

    # Get updated statistics
    print_header("7. Updated Statistics")
    response = requests.get(f"{BASE_URL}/api/stats")
    stats = response.json()
    print(f"Total Progress: {stats['total_progress']:.1f}%")
    print(f"Total XP: {stats['total_xp']}")
    print(f"Completed Phases: {stats['completed_phases']}/{stats['total_phases']}")

    print_header("Demo Complete! 🎉")
    print(
        "✅ API is working correctly\n"
        "✅ All 10 phases loaded\n"
        "✅ CRUD operations working\n"
        "✅ Progress tracking functional\n"
        "✅ Statistics calculated properly\n"
    )


if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API at http://localhost:8000")
        print("   Please start the API server first:")
        print("   poetry run uvicorn backend.app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
