# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Personal Skill Tracker                   │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │      │   Backend    │      │     CLI      │
│  (Next.js)   │◄────►│  (FastAPI)   │◄────►│   (Typer)    │
│  Port 3000   │      │  Port 8000   │      │   Terminal   │
└──────────────┘      └──────────────┘      └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │   SQLite DB  │
                      │ skill_tracker│
                      └──────────────┘
```

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 14**: React framework with server-side rendering
- **React 18**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript
- **Axios**: HTTP client

### CLI
- **Typer**: CLI framework
- **Rich**: Beautiful terminal formatting
- **Click**: Command-line interface creation kit

### Development Tools
- **Pytest**: Testing framework
- **Black**: Code formatter
- **Pylint**: Code linter
- **ESLint**: JavaScript/TypeScript linter
- **GitHub Actions**: CI/CD pipeline

## Database Schema

```
┌───────────┐      ┌──────────┐      ┌────────────┐      ┌──────────────────┐
│  Phases   │─────►│  Topics  │─────►│ Subtopics  │─────►│ MasteryComponents│
└───────────┘      └──────────┘      └────────────┘      └──────────────────┘
     │                  │                    │                      │
     └──────────────────┴────────────────────┴──────────────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │   Progress   │◄───┐
                      └──────────────┘    │
                              │           │
                              ▼           │
                      ┌──────────────┐    │
                      │    Notes     │────┘
                      └──────────────┘

     ┌──────────────┐        ┌──────────┐
     │ Achievements │        │  Stats   │
     └──────────────┘        └──────────┘
```

## API Endpoints Structure

### Phases (10 roadmap phases)
- GET    /api/phases
- GET    /api/phases/{id}
- POST   /api/phases
- PUT    /api/phases/{id}
- DELETE /api/phases/{id}

### Topics (Learning topics within phases)
- GET    /api/topics?phase_id={id}
- GET    /api/topics/{id}
- POST   /api/topics
- PUT    /api/topics/{id}
- DELETE /api/topics/{id}

### Subtopics (Specific learning items)
- GET    /api/subtopics?topic_id={id}
- GET    /api/subtopics/{id}
- POST   /api/subtopics
- PUT    /api/subtopics/{id}
- DELETE /api/subtopics/{id}

### Mastery Components (Theory, Practice, Project)
- GET    /api/mastery-components?subtopic_id={id}
- GET    /api/mastery-components/{id}
- POST   /api/mastery-components
- PUT    /api/mastery-components/{id}
- DELETE /api/mastery-components/{id}

### Progress & Notes
- GET    /api/progress
- POST   /api/progress
- PUT    /api/progress/{id}
- GET    /api/notes?progress_id={id}
- POST   /api/notes

### Dashboard & Analytics
- GET    /api/dashboard      # Complete dashboard data
- GET    /api/stats          # Overall statistics
- GET    /api/achievements   # All achievements
- GET    /api/export         # Export all data as JSON

## CLI Commands

```bash
# List commands
cli.main list-phases              # Show all 10 phases
cli.main list-topics              # Show all topics
cli.main list-topics --phase-id 1 # Topics in phase 1
cli.main list-subtopics           # Show all subtopics
cli.main list-subtopics --topic-id 1

# Progress tracking
cli.main update-progress <subtopic_id> \
  --status in_progress \
  --percentage 50 \
  --hours 2.5

# Notes
cli.main add-note <subtopic_id> "Note content here"

# Dashboard & Stats
cli.main dashboard    # Full dashboard with progress
cli.main stats        # Detailed statistics
cli.main achievements # Show all achievements

# Export
cli.main export --output-file my_progress.json
```

## Data Flow

### User Updates Progress (CLI)
```
User → CLI → Database → Update Stats → Check Achievements
                 ↓
           Update Progress
```

### View Dashboard (Frontend)
```
Browser → Next.js → API Request → FastAPI → Database
                                      ↓
Browser ← Next.js ← JSON Response ← Process Data
```

### Export Data (API/CLI)
```
Request → FastAPI → Query all tables → Format JSON → Response
```

## Gamification System

### Achievements
- 🎯 First Step (10 pts) - Complete first subtopic
- 🚀 Getting Started (50 pts) - Complete 5 subtopics
- 🏆 Phase Master (100 pts) - Complete entire phase
- 📚 Dedicated Learner (50 pts) - Study 10 hours
- 🎓 Marathon Learner (200 pts) - Study 100 hours
- 🔥 Streak Master (75 pts) - 7-day streak

### Statistics Tracked
- Total points earned
- Total hours studied
- Current study streak
- Longest study streak
- Phases/topics/subtopics completed

## File Structure

```
personal-skill-polish/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models (8 models)
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── api/             # API routes (future)
│   │   ├── db/              # Database connection
│   │   ├── main.py          # FastAPI app (40+ endpoints)
│   │   └── seed_data.py     # Initialize with 10 phases
│   └── tests/
│       └── test_api.py      # 10 API tests
├── frontend/
│   ├── pages/
│   │   ├── index.tsx        # Dashboard
│   │   ├── phases/          # Phase pages
│   │   └── _app.tsx         # App wrapper
│   └── styles/
│       └── globals.css      # Tailwind styles
├── cli/
│   └── main.py              # Typer CLI (9 commands)
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline
├── requirements.txt         # Python deps
├── package.json            # Node deps (frontend)
└── README.md               # Documentation
```

## Development Workflow

1. **Start Backend**: `uvicorn backend.app.main:app --reload`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Use CLI**: `python -m cli.main dashboard`
4. **Run Tests**: `pytest backend/tests/`
5. **Format Code**: `black backend/ cli/`

## Testing Strategy

### Backend Tests (Pytest)
- Unit tests for each API endpoint
- Integration tests for workflows
- Database transaction tests
- 10 tests covering CRUD operations

### Frontend Tests (Future)
- Component tests with React Testing Library
- E2E tests with Playwright
- Accessibility tests

### CI/CD Pipeline
- Automated tests on push/PR
- Code quality checks (black, pylint)
- Coverage reporting
- Build verification

## Security Considerations

- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration for API
- No sensitive data in repository
- Database file in .gitignore

## Performance Optimizations

- SQLite for lightweight operations
- Efficient database queries
- Frontend API caching
- Lazy loading for frontend components
- Background job processing for stats updates

## Future Enhancements

- [ ] User authentication
- [ ] Multi-user support
- [ ] Cloud sync
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Social features
- [ ] Study reminders
- [ ] Spaced repetition algorithm
- [ ] Resource recommendations
- [ ] Progress visualization charts
