#!/bin/bash

# Setup script for RPG Maestro

echo "Setting up RPG Maestro project..."

# Create necessary directories if they don't exist
mkdir -p api/game
mkdir -p frontend/pages
mkdir -p frontend/components
mkdir -p frontend/styles
mkdir -p frontend/public
mkdir -p static/audio

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file and add your API keys"
fi

echo "Setup complete! Next steps:"
echo "1. Edit the .env file with your API keys"
echo "2. Run the backend: uvicorn api.main:app --reload"
echo "3. Run the frontend: cd frontend && npm run dev"
echo "4. Visit http://localhost:3000 in your browser"
