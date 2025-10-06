# Personal Skill Polish Tracker 🚀

A comprehensive full-stack application for tracking your AI/ML System Design learning journey from Strong Python Developer → AI Systems Architect.

## 📋 Overview

This system helps you track, visualize, and master all 10 phases of your AI/ML system design roadmap with:

- **Backend**: FastAPI (Python 3.11+) with Pydantic models
- **Frontend**: Next.js + TailwindCSS + shadcn/ui + Recharts
- **Database**: SQLite for local persistence
- **CLI**: Typer-based command-line tool (skillcli)
- **Testing**: pytest with coverage
- **Code Quality**: Ruff, Black, and mypy
- **CI/CD**: GitHub Actions

## 🎯 10-Phase Roadmap

1. **Core Computer Science Foundation** - Data Structures, Algorithms
2. **Python Engineering Mastery** - Advanced Python Core, OOP, Tooling
3. **Machine Learning Foundations** - Linear Models, Trees, Neural Networks, Optimization
4. **Deep Learning Engineering** - CNNs, RNNs, Transformers, Deployment
5. **Data Infrastructure** - Data Lakes, ETL, Streaming, Databases
6. **ML Systems Engineering** - Model Serving, Feature Stores, Orchestration, Versioning
7. **AI Infrastructure** - GPU/TPU programming, CUDA, Dask, Ray, Kubernetes, Cloud AI
8. **Advanced AI Architectures** - Microservices, RPC, Messaging, Observability, Fault tolerance
9. **AI Systems at Scale** - High availability, Scaling, Latency optimization, Resource orchestration
10. **AI Leadership & Strategy** - System design leadership, Roadmap planning, Ethics

## 🏗️ Project Structure

```
personal-skill-polish/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── crud.py            # CRUD operations
│   │   └── database.py        # Database configuration
│   ├── cli.py                 # Typer CLI tool
│   └── tests/
│       └── test_api.py        # API tests
├── frontend/
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── Dashboard.tsx      # Analytics dashboard
│   │   └── PhasesList.tsx     # Phases list view
│   └── lib/
│       └── utils.ts           # Utility functions
├── .github/
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
├── roadmap.json               # Example roadmap data
├── pyproject.toml             # Python dependencies
└── README.md

```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Poetry (for Python dependency management)

### Backend Setup

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Initialize database with roadmap:**
   ```bash
   poetry run skillcli init --file roadmap.json
   ```

3. **Start the API server:**
   ```bash
   poetry run uvicorn backend.app.main:app --reload
   ```

   API will be available at: http://localhost:8000
   
   API docs: http://localhost:8000/docs

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

### CLI Usage

The CLI tool provides offline access to track your progress:

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
poetry run skillcli export --output roadmap_backup.json --format json
poetry run skillcli export --output roadmap_backup.yaml --format yaml
```

## 📊 Features

### Core Features
- ✅ **CRUD Operations** - Create, read, update, delete phases, topics, and subtopics
- ✅ **Progress Tracking** - Track completion percentage for each phase and topic
- ✅ **Analytics Dashboard** - Visualize progress with interactive charts
- ✅ **Notes & Reflections** - Add personal notes and reflections for each topic
- ✅ **CLI Interface** - Offline updates via command-line tool
- ✅ **Export/Import** - JSON/YAML roadmap export and import
- ✅ **Gamification** - XP points and progress tracking

### Data Model
- **Phases**: High-level learning phases with title, goal, progress, notes, and XP
- **Topics**: Specific topics within phases with subtopics and mastery components
- **Subtopics**: Detailed learning items with completion status
- **Mastery Components**: Skills to master with 0-5 level scale

## 🧪 Testing

Run backend tests:
```bash
poetry run pytest backend/tests/ -v --cov=backend
```

Generate coverage report:
```bash
poetry run pytest backend/tests/ --cov=backend --cov-report=html
```

## 🎨 Code Quality

Format code:
```bash
poetry run black backend/
```

Lint code:
```bash
poetry run ruff check backend/
```

Type checking:
```bash
poetry run mypy backend/
```

## 🔧 API Endpoints

### Phases
- `GET /api/phases` - List all phases
- `GET /api/phases/{id}` - Get phase details
- `POST /api/phases` - Create new phase
- `PATCH /api/phases/{id}` - Update phase
- `DELETE /api/phases/{id}` - Delete phase

### Topics
- `GET /api/topics/{id}` - Get topic details
- `POST /api/phases/{phase_id}/topics` - Create topic
- `PATCH /api/topics/{id}` - Update topic
- `DELETE /api/topics/{id}` - Delete topic

### Subtopics
- `GET /api/subtopics/{id}` - Get subtopic details
- `POST /api/topics/{topic_id}/subtopics` - Create subtopic
- `PATCH /api/subtopics/{id}` - Update subtopic
- `DELETE /api/subtopics/{id}` - Delete subtopic

### Mastery Components
- `GET /api/mastery/{id}` - Get mastery component
- `POST /api/topics/{topic_id}/mastery` - Create mastery component
- `PATCH /api/mastery/{id}` - Update mastery component
- `DELETE /api/mastery/{id}` - Delete mastery component

### Statistics
- `GET /api/stats` - Get overall progress statistics

## 🌐 Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
DATABASE_URL=sqlite:///./skill_polish.db

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📦 Deployment

### Backend (Example with Docker)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY backend/ ./backend/
CMD ["poetry", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Vercel)
The frontend can be easily deployed to Vercel:
```bash
cd frontend
vercel deploy
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is for personal use.

## 🎓 Learning Path

The tracker is designed to guide you through a comprehensive AI/ML systems design journey:

1. **Foundations** (Phases 1-3): Build core CS and ML fundamentals
2. **Deep Learning** (Phase 4): Master modern neural architectures
3. **Infrastructure** (Phases 5-7): Learn data and AI infrastructure
4. **Architecture** (Phases 8-9): Design production-scale AI systems
5. **Leadership** (Phase 10): Lead AI initiatives and strategy

## 🔮 Future Enhancements

- [ ] Authentication and multi-user support
- [ ] Badges and achievements system
- [ ] Progress reminders and notifications
- [ ] Study time tracking
- [ ] Resource links for each topic
- [ ] Community features (share progress)
- [ ] Mobile app (React Native)
- [ ] Integration with learning platforms

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy Learning! 🚀 From Python Developer → AI Systems Architect**
