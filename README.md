# 🎯 Personal Skill Tracker

A comprehensive full-stack application for tracking your learning journey through the **ULTIMATE AI/ML SYSTEM DESIGN ROADMAP** covering all 10 phases from Core CS Foundations to AI Leadership.

## 🌟 Features

### Core Functionality
- **10 AI/ML Phases**: From Core CS Foundations to AI Leadership
- **Hierarchical Learning Structure**: Phases → Topics → Subtopics → Mastery Components
- **Progress Tracking**: Track status, completion percentage, and hours spent
- **Note Taking**: Add notes to your progress at any level
- **Gamification**: Earn points, unlock achievements, and maintain learning streaks

### Technology Stack
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: Next.js 14 + React + Tailwind CSS
- **CLI**: Typer + Rich (beautiful terminal UI)
- **Testing**: Pytest + Coverage
- **CI/CD**: GitHub Actions

## 📁 Project Structure

```
personal-skill-polish/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── schemas/         # Pydantic schemas for validation
│   │   ├── api/             # API route handlers
│   │   ├── db/              # Database connection & session
│   │   ├── main.py          # FastAPI application
│   │   └── seed_data.py     # Initialize database with roadmap data
│   └── tests/
│       └── test_api.py      # API tests
├── frontend/
│   ├── pages/
│   │   ├── index.tsx        # Dashboard page
│   │   ├── phases/          # Phases pages
│   │   └── _app.tsx         # App wrapper
│   ├── styles/
│   │   └── globals.css      # Global styles with Tailwind
│   └── package.json
├── cli/
│   └── main.py              # Typer CLI application
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Python project configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Initialize the database with sample data**:
```bash
python -m backend.app.seed_data
```

3. **Start the FastAPI server**:
```bash
python -m backend.app.main
# Or with uvicorn directly:
uvicorn backend.app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install Node.js dependencies**:
```bash
npm install
```

3. **Start the development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### CLI Usage

The CLI provides a convenient way to interact with your skill tracker from the terminal.

**List all phases**:
```bash
python -m cli.main list-phases
```

**List topics** (optionally filter by phase):
```bash
python -m cli.main list-topics
python -m cli.main list-topics --phase-id 1
```

**List subtopics** (optionally filter by topic):
```bash
python -m cli.main list-subtopics
python -m cli.main list-subtopics --topic-id 1
```

**Update progress**:
```bash
python -m cli.main update-progress 1 --status in_progress --percentage 50 --hours 2.5
```

**Add a note**:
```bash
python -m cli.main add-note 1 "Completed the theory section"
```

**View dashboard**:
```bash
python -m cli.main dashboard
```

**View statistics**:
```bash
python -m cli.main stats
```

**View achievements**:
```bash
python -m cli.main achievements
```

**Export data to JSON**:
```bash
python -m cli.main export --output-file my_progress.json
```

## 📊 API Endpoints

### Phases
- `GET /api/phases` - List all phases
- `GET /api/phases/{id}` - Get phase details
- `POST /api/phases` - Create new phase
- `PUT /api/phases/{id}` - Update phase
- `DELETE /api/phases/{id}` - Delete phase

### Topics
- `GET /api/topics?phase_id={id}` - List topics (optionally filtered)
- `GET /api/topics/{id}` - Get topic details
- `POST /api/topics` - Create new topic
- `PUT /api/topics/{id}` - Update topic
- `DELETE /api/topics/{id}` - Delete topic

### Subtopics
- `GET /api/subtopics?topic_id={id}` - List subtopics
- `GET /api/subtopics/{id}` - Get subtopic details
- `POST /api/subtopics` - Create new subtopic
- `PUT /api/subtopics/{id}` - Update subtopic
- `DELETE /api/subtopics/{id}` - Delete subtopic

### Mastery Components
- `GET /api/mastery-components?subtopic_id={id}` - List mastery components
- `GET /api/mastery-components/{id}` - Get component details
- `POST /api/mastery-components` - Create new component
- `PUT /api/mastery-components/{id}` - Update component
- `DELETE /api/mastery-components/{id}` - Delete component

### Progress & Notes
- `GET /api/progress` - List all progress records
- `POST /api/progress` - Create progress record
- `PUT /api/progress/{id}` - Update progress
- `GET /api/notes?progress_id={id}` - List notes
- `POST /api/notes` - Create note

### Dashboard & Stats
- `GET /api/dashboard` - Get dashboard data (stats, progress, achievements)
- `GET /api/stats` - Get overall statistics
- `GET /api/achievements` - Get achievements
- `GET /api/export` - Export all data as JSON

## 🎓 The AI/ML Roadmap (10 Phases)

1. **Phase 1: Core CS Foundations** - Data Structures, Algorithms, System Design Basics
2. **Phase 2: Mathematics for ML** - Linear Algebra, Probability, Calculus, Optimization
3. **Phase 3: Machine Learning Fundamentals** - Supervised & Unsupervised Learning
4. **Phase 4: Deep Learning** - Neural Networks, CNNs, RNNs, Transformers
5. **Phase 5: ML Engineering** - Model Training, MLOps, Deployment
6. **Phase 6: AI System Architecture** - Distributed Systems, Real-time AI
7. **Phase 7: Data Engineering for AI** - Data Pipelines, Feature Stores
8. **Phase 8: Advanced AI Topics** - Reinforcement Learning, Generative AI
9. **Phase 9: AI Ethics & Safety** - Fairness, Bias, AI Safety
10. **Phase 10: AI Leadership & Strategy** - Product Management, Team Building

Each phase contains multiple topics, and each topic has several subtopics with mastery components (Theory, Practice, Project).

## 🧪 Testing

### Run Backend Tests
```bash
pytest backend/tests/ -v --cov=backend/app
```

### Run Linting
```bash
# Python
black backend/
pylint backend/app/

# Frontend
cd frontend
npm run lint
```

## 🔄 CI/CD

The project includes a GitHub Actions workflow that:
- Runs tests on every push and pull request
- Checks code quality with linting
- Generates coverage reports
- Tests both backend and frontend

## 📝 Development Workflow

1. **Start Backend**: `uvicorn backend.app.main:app --reload`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Use CLI**: `python -m cli.main dashboard`
4. **Run Tests**: `pytest backend/tests/`
5. **Check Code**: `black backend/ && pylint backend/app/`

## 🎮 Gamification Features

- **Points System**: Earn points for completing subtopics and studying
- **Achievements**: Unlock badges for milestones (First Step, Phase Master, etc.)
- **Streaks**: Track daily study streaks
- **Progress Bars**: Visual progress tracking for each phase
- **Statistics Dashboard**: Comprehensive stats on your learning journey

## 🛠️ Customization

You can customize the roadmap by:
1. Editing `backend/app/seed_data.py` to add/modify phases, topics, and subtopics
2. Running the seed script again to update the database
3. The frontend and CLI will automatically reflect the changes

## 📄 License

This is a personal project for skill tracking and learning management.

## 🤝 Contributing

This is a personal learning tracker, but feel free to fork and adapt it for your own needs!

---

**Built with ❤️ for continuous learning and skill development**