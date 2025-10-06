# Quick Start Guide

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed (for frontend)
- Git installed

## 5-Minute Setup

### Step 1: Clone and Install

```bash
# Install backend dependencies
pip install poetry
poetry install

# Install frontend dependencies (optional)
cd frontend
npm install
cd ..
```

### Step 2: Load Initial Data

```bash
# Load the 10-phase AI/ML roadmap
poetry run python backend/load_roadmap.py roadmap.json
```

When prompted, type 'y' to confirm.

### Step 3: Start the Backend

```bash
poetry run uvicorn backend.app.main:app --reload
```

The API will be available at http://localhost:8000

### Step 4: Start the Frontend (Optional)

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:3000

## Using the System

### Via Web Interface

1. Open http://localhost:3000
2. View dashboard with progress charts
3. Expand phases to see topics and subtopics
4. Track your progress visually

### Via API

Access the interactive API documentation at http://localhost:8000/docs

Example API calls:
```bash
# Get all phases
curl http://localhost:8000/api/phases

# Get statistics
curl http://localhost:8000/api/stats

# Update phase progress
curl -X PATCH http://localhost:8000/api/phases/1 \
  -H "Content-Type: application/json" \
  -d '{"progress": 50.0, "xp": 100}'
```

### Via CLI

```bash
# List all phases
poetry run skillcli list-phases

# Show phase details
poetry run skillcli show-phase 1

# Update progress
poetry run skillcli update-progress 1 --progress 50 --xp 100

# Add notes
poetry run skillcli add-note 1 --note "Completed data structures module"

# View statistics
poetry run skillcli stats

# Export roadmap
poetry run skillcli export --output backup.json --format json
```

## Running the Demo

```bash
python demo.py
```

This will demonstrate all API features with sample data.

## Running Tests

```bash
# Run all tests
poetry run pytest backend/tests/ -v

# With coverage
poetry run pytest backend/tests/ --cov=backend --cov-report=html
```

## Code Quality

```bash
# Format code
poetry run black backend/

# Lint code
poetry run ruff check backend/

# Type checking
poetry run mypy backend/
```

## What's Included

✅ **10 AI/ML System Design Phases**
- Core Computer Science Foundation
- Python Engineering Mastery
- Machine Learning Foundations
- Deep Learning Engineering
- Data Infrastructure
- ML Systems Engineering
- AI Infrastructure
- Advanced AI Architectures
- AI Systems at Scale
- AI Leadership & Strategy

✅ **Multiple Topics per Phase** with:
- Subtopics with completion tracking
- Mastery components (0-5 level scale)
- Progress percentage
- XP points
- Notes and reflections

✅ **Full-Stack Application**
- REST API with FastAPI
- React dashboard with charts
- Command-line interface
- SQLite database

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed: `python --version`
- Install Poetry: `pip install poetry`
- Install dependencies: `poetry install`

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Install dependencies: `cd frontend && npm install`

### Database issues
- Delete `skill_polish.db` and reload: `poetry run python backend/load_roadmap.py roadmap.json`

### Port conflicts
- Backend: Change port in uvicorn command: `--port 8001`
- Frontend: Change port in package.json or use: `PORT=3001 npm run dev`

## Next Steps

1. **Start Learning**: Begin with Phase 1 (Core Computer Science Foundation)
2. **Track Progress**: Update progress as you complete topics
3. **Add Notes**: Document your learnings and reflections
4. **Set Goals**: Aim for consistent XP gains
5. **Review Stats**: Monitor your overall progress regularly

## Support

- 📖 Full Documentation: See `README.md`
- 🔧 API Docs: http://localhost:8000/docs
- 📝 Implementation Details: See `IMPLEMENTATION.md`

Happy Learning! 🚀
