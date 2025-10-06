#!/bin/bash

# Personal Skill Polish Tracker - Setup Script
# This script sets up the entire project

set -e

echo "🚀 Setting up Personal Skill Polish Tracker..."
echo ""

# Check for Python 3.11+
echo "📦 Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2)
echo "Found Python $python_version"

# Install Poetry if not available
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✓ Poetry already installed"
fi

# Install backend dependencies
echo ""
echo "📦 Installing backend dependencies..."
poetry install --no-interaction

# Create database and load roadmap
echo ""
echo "📊 Initializing database..."
if [ -f "roadmap.json" ]; then
    poetry run python backend/load_roadmap.py roadmap.json <<< "y"
else
    echo "⚠️  roadmap.json not found, skipping database initialization"
fi

# Check for Node.js
echo ""
echo "📦 Checking Node.js..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "Found Node.js $node_version"
    
    # Install frontend dependencies
    echo ""
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "⚠️  Node.js not found, skipping frontend setup"
    echo "   Install Node.js 18+ to set up the frontend"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Start the backend API:"
echo "   poetry run uvicorn backend.app.main:app --reload"
echo ""
echo "2. Start the frontend (in a new terminal):"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "4. Use the CLI:"
echo "   poetry run skillcli list-phases"
echo "   poetry run skillcli stats"
echo ""
