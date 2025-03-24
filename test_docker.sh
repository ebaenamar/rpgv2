#!/bin/bash

# Colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
NC="\033[0m" # No Color

echo -e "${YELLOW}=== RPG Maestro Docker Test Suite ===${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
  exit 1
fi

# Check if the image exists
if [[ "$(docker images -q rpg-maestro-api:latest 2> /dev/null)" == "" ]]; then
  echo -e "${YELLOW}Building Docker image...${NC}"
  docker build -t rpg-maestro-api .
  if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to build Docker image.${NC}"
    exit 1
  fi
fi

# Start the container using docker-compose
echo -e "${YELLOW}Starting Docker container...${NC}"
docker-compose -f docker-compose.test.yml up -d

if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to start Docker container.${NC}"
  exit 1
fi

echo -e "${GREEN}Container started. Waiting for API to initialize...${NC}"
sleep 5

# Run the Python test script
echo -e "${YELLOW}Running API tests...${NC}"
python docker_test_detailed.py
TEST_RESULT=$?

# Stop the container
echo -e "${YELLOW}Stopping Docker container...${NC}"
docker-compose -f docker-compose.test.yml down

# Final report
echo -e "\n${YELLOW}=== Docker Test Report ===${NC}"
if [ $TEST_RESULT -eq 0 ]; then
  echo -e "${GREEN}✅ All tests passed! The Docker container is working correctly.${NC}"
  echo -e "${GREEN}The backend is ready for deployment to Render.${NC}"
else
  echo -e "${RED}❌ Some tests failed. Please check the logs above for details.${NC}"
  echo -e "${YELLOW}Fix the issues before deploying to Render.${NC}"
fi

# Instructions for deployment
echo -e "\n${YELLOW}=== Next Steps ===${NC}"
echo -e "1. Make sure you have real API keys in your Render environment variables"
echo -e "2. Push your changes to GitHub:"
echo -e "   ${GREEN}git add . && git commit -m \"chore: deploy memories\" && git push${NC}"
echo -e "3. Deploy to Render through the Render dashboard"

exit $TEST_RESULT
