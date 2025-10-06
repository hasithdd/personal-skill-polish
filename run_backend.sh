#!/bin/bash

# Quick start script for Personal Skill Tracker

echo "🎯 Starting Personal Skill Tracker..."
echo ""

# Start backend in background
echo "Starting backend API on http://localhost:8000..."
cd "$(dirname "$0")"
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Backend logs will appear below:"
echo ""
echo "To stop the backend, run: kill $BACKEND_PID"
echo ""
echo "For frontend, run in another terminal:"
echo "  cd frontend && npm run dev"
echo ""

# Wait for backend
wait $BACKEND_PID
