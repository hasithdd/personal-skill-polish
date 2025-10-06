#!/bin/bash

echo "🎯 Personal Skill Tracker - Setup Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Check Node.js version
echo "Checking Node.js version..."
node_version=$(node --version 2>&1)
echo "✓ Node.js $node_version found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python -m backend.app.seed_data

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  Backend:  uvicorn backend.app.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo "  CLI:      python -m cli.main dashboard"
echo ""
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
