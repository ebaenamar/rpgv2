#!/bin/bash

# Stop any running containers
docker-compose -f docker-compose.test.yml down

# Start the backend API
docker-compose -f docker-compose.test.yml up -d

# Create a temporary .env.local file for the frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > frontend/.env.local

# Start the frontend
cd frontend && npm run dev
