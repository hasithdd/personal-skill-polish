# Quick Reference Guide

## 🚀 Quick Start (3 Steps)

```bash
# 1. Setup
pip install -r requirements.txt
python -m backend.app.seed_data

# 2. Start Backend
uvicorn backend.app.main:app --reload

# 3. Use CLI
python -m cli.main dashboard
```

## 📋 Common CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list-phases` | Show all phases | `python -m cli.main list-phases` |
| `list-topics` | Show topics | `python -m cli.main list-topics --phase-id 1` |
| `list-subtopics` | Show subtopics | `python -m cli.main list-subtopics --topic-id 1` |
| `update-progress` | Update progress | `python -m cli.main update-progress 1 --status in_progress --percentage 50 --hours 2` |
| `add-note` | Add a note | `python -m cli.main add-note 1 "Completed theory"` |
| `dashboard` | View dashboard | `python -m cli.main dashboard` |
| `stats` | View statistics | `python -m cli.main stats` |
| `achievements` | View achievements | `python -m cli.main achievements` |
| `export` | Export data | `python -m cli.main export --output-file data.json` |

## 🔗 API Endpoints (Quick Reference)

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/phases` | GET | List all phases |
| `/api/phases/{id}` | GET | Get phase details |
| `/api/topics?phase_id={id}` | GET | List topics |
| `/api/subtopics?topic_id={id}` | GET | List subtopics |
| `/api/progress` | GET/POST | Progress records |
| `/api/dashboard` | GET | Dashboard data |
| `/api/stats` | GET | Statistics |
| `/api/export` | GET | Export JSON |
| `/docs` | GET | API documentation |

## 🎯 Status Values

- `not_started` - Haven't started yet
- `in_progress` - Currently learning
- `completed` - Finished

## 💡 Tips & Tricks

### Backend Development
```bash
# Run with auto-reload
uvicorn backend.app.main:app --reload --port 8000

# View API docs
# Open http://localhost:8000/docs in browser

# Test API with curl
curl http://localhost:8000/api/phases | jq
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev  # Start on http://localhost:3000
npm run build  # Build for production
npm run lint  # Check code quality
```

### Testing
```bash
# Run all tests
pytest backend/tests/ -v

# Run with coverage
pytest backend/tests/ --cov=backend/app

# Run specific test
pytest backend/tests/test_api.py::test_create_phase -v
```

### Code Quality
```bash
# Format code
black backend/ cli/

# Check formatting
black --check backend/ cli/

# Lint code
pylint backend/app/
```

## 📊 Database Info

- **File**: `skill_tracker.db` (created automatically)
- **Tables**: 8 (Phase, Topic, Subtopic, MasteryComponent, Progress, Note, Achievement, Stats)
- **Pre-seeded**: 10 phases, 20 topics, 67 subtopics, 201 mastery components, 6 achievements

## 🎮 Gamification

### Points
- Complete subtopic: +10 points
- Complete topic: +50 points
- Complete phase: +100 points
- Daily streak: +5 points/day

### Achievements
- 🎯 First Step (10 pts)
- 🚀 Getting Started (50 pts)
- 🏆 Phase Master (100 pts)
- 📚 Dedicated Learner (50 pts)
- 🎓 Marathon Learner (200 pts)
- 🔥 Streak Master (75 pts)

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI application |
| `backend/app/models/__init__.py` | Database models |
| `backend/app/seed_data.py` | Initialize database |
| `cli/main.py` | CLI application |
| `frontend/pages/index.tsx` | Dashboard page |
| `requirements.txt` | Python dependencies |

## 🛠️ Troubleshooting

### "Database locked" error
```bash
# Close all database connections
# Delete skill_tracker.db and re-run:
python -m backend.app.seed_data
```

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules .next
npm install
```

### Tests failing
```bash
# Ensure test database is clean
rm -f test.db
pytest backend/tests/
```

## 📚 Learning the Codebase

### Start Here
1. Read `README.md` for overview
2. Check `ARCHITECTURE.md` for system design
3. Explore `backend/app/models/__init__.py` for data models
4. Look at `backend/app/main.py` for API endpoints
5. Try `cli/main.py` commands

### Key Concepts
- **Phase**: Major learning stage (e.g., "Deep Learning")
- **Topic**: Subject within a phase (e.g., "Neural Networks")
- **Subtopic**: Specific item to learn (e.g., "Backpropagation")
- **Mastery Component**: Theory, Practice, or Project for each subtopic
- **Progress**: Tracks status, percentage, hours spent

## 🚧 Common Tasks

### Add a new phase
```bash
curl -X POST http://localhost:8000/api/phases \
  -H "Content-Type: application/json" \
  -d '{"name": "New Phase", "description": "Description", "order": 11}'
```

### Update progress via API
```bash
curl -X PUT http://localhost:8000/api/progress/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "completion_percentage": 100}'
```

### Export your progress
```bash
# Via CLI
python -m cli.main export --output-file my_progress.json

# Via API
curl http://localhost:8000/api/export > progress.json
```

## 🎨 Customization

### Change the roadmap
Edit `backend/app/seed_data.py` and modify the `phases_data` list, then:
```bash
# Backup current database
mv skill_tracker.db skill_tracker.db.backup

# Reseed
python -m backend.app.seed_data
```

### Add custom achievements
Edit `backend/app/seed_data.py`, add to `achievements_data`, then reseed.

### Modify UI colors
Edit `frontend/tailwind.config.js` to change the color scheme.

## 📞 Getting Help

1. Check the `README.md` for detailed documentation
2. View API docs at `http://localhost:8000/docs`
3. Review test files for usage examples
4. Check `ARCHITECTURE.md` for system design

## 🔄 Version Control

```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main
```

---

**Pro Tip**: Use `python -m cli.main dashboard` daily to track your progress! 🎯
