#!/bin/bash

# AI News Avatar Pipeline - Startup Script

echo "=========================================="
echo "AI News Avatar Video Generator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found."
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found."
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys before continuing!"
    echo "   - OPENAI_API_KEY"
    echo "   - DID_API_KEY"
    echo ""
    exit 1
fi

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Start the server
echo "=========================================="
echo "Starting FastAPI server..."
echo "=========================================="
echo ""
echo "Server will be available at:"
echo "  → http://localhost:8000"
echo "  → API Docs: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Run uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000