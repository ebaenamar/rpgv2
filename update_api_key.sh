#!/bin/bash

# Script to update AI21 API key in .env.docker file

ENV_FILE=".env.docker"

# Check if the environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE does not exist."
    exit 1
fi

# Prompt for the API key (will not be displayed in terminal)
echo "Enter your AI21 API key (input will be hidden):"
read -s API_KEY
echo ""

if [ -z "$API_KEY" ]; then
    echo "Error: API key cannot be empty."
    exit 1
fi

# Update the API key in the environment file
if grep -q "^AI21_API_KEY=" "$ENV_FILE"; then
    # Replace existing API key
    sed -i '' "s/^AI21_API_KEY=.*/AI21_API_KEY=$API_KEY/" "$ENV_FILE"
else
    # Add API key if it doesn't exist
    echo "AI21_API_KEY=$API_KEY" >> "$ENV_FILE"
fi

echo "API key has been updated in $ENV_FILE"
