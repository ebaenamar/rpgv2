#!/bin/bash

# This script tests the frontend-backend integration for RPG Maestro

# Step 1: Ensure backend API is running
echo "===== Step 1: Checking backend API status ====="
BACKEND_URL="http://localhost:8080/api/scene/intro"
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BACKEND_URL)

if [ $BACKEND_STATUS -eq 200 ]; then
  echo "✅ Backend API is running at $BACKEND_URL"
else
  echo "❌ Backend API is not running or not accessible at $BACKEND_URL"
  echo "Starting backend API..."
  docker-compose -f docker-compose.test.yml up -d
  sleep 5
  BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BACKEND_URL)
  
  if [ $BACKEND_STATUS -eq 200 ]; then
    echo "✅ Backend API is now running"
  else
    echo "❌ Failed to start backend API. Please check Docker logs."
    exit 1
  fi
fi

# Step 2: Create frontend environment file
echo "\n===== Step 2: Setting up frontend environment ====="
FRONTEND_ENV="frontend/.env.local"

echo "Creating $FRONTEND_ENV file..."
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > $FRONTEND_ENV
echo "✅ Created frontend environment file"

# Step 3: Start frontend development server
echo "\n===== Step 3: Starting frontend development server ====="
echo "Starting frontend server..."
cd frontend && npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend server started with PID: $FRONTEND_PID"

# Step 4: Wait for frontend to be ready
echo "\n===== Step 4: Waiting for frontend to be ready ====="
sleep 10
echo "✅ Frontend should be ready now at http://localhost:3000"

# Step 5: Provide testing instructions
echo "\n===== Step 5: Testing Instructions ====="
echo "Please test the following features:"
echo "1. Start a new game by clicking 'Begin Your Adventure'"
echo "2. Verify that the scene image is generated correctly"
echo "3. Make a choice and verify that the character response appears in a comic-style vignette"
echo "4. Test the audio playback by clicking the play button"
echo "5. Verify that scene transitions work correctly"

echo "\nWhen you're done testing, press Enter to stop the frontend server..."
read

# Step 6: Clean up
echo "\n===== Step 6: Cleaning up ====="
kill $FRONTEND_PID
echo "✅ Frontend server stopped"

echo "\n===== Testing completed ====="
