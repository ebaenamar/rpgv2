#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse

# Base URL for the API
API_URL = "http://localhost:8080/api"

def test_scene_endpoint():
    """Test the scene endpoint"""
    print("\n===== Testing Scene Endpoint =====")
    try:
        response = requests.get(f"{API_URL}/scene/intro")
        response.raise_for_status()
        data = response.json()
        print("✅ Scene endpoint working!")
        print(f"Scene ID: {data['scene']['scene_id']}")
        print(f"Choices: {len(data['choices'])}")
        print(f"Image URL: {data['image_url']}")
        return True
    except Exception as e:
        print(f"❌ Scene endpoint failed: {e}")
        return False

def test_objectives_endpoint():
    """Test the objectives endpoint"""
    print("\n===== Testing Objectives Endpoint =====")
    try:
        response = requests.get(f"{API_URL}/objectives")
        response.raise_for_status()
        data = response.json()
        print("✅ Objectives endpoint working!")
        print(f"Number of objectives: {len(data['objectives'])}")
        return True
    except Exception as e:
        print(f"❌ Objectives endpoint failed: {e}")
        return False

def test_action_endpoint():
    """Test the action endpoint"""
    print("\n===== Testing Action Endpoint =====")
    try:
        payload = {
            "scene_id": "intro",
            "choice_index": 0
        }
        response = requests.post(f"{API_URL}/action", json=payload)
        response.raise_for_status()
        data = response.json()
        print("✅ Action endpoint working!")
        print(f"Next scene: {data['next_scene_id']}")
        print(f"Agent response: {data['agent_response'][:50]}...")
        if 'scoring' in data:
            print(f"Scoring feedback: {data['scoring']['feedback'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Action endpoint failed: {e}")
        return False

def test_image_generation():
    """Test the image generation functionality"""
    print("\n===== Testing Image Generation =====")
    try:
        # First get a scene to check if it has a real image URL
        response = requests.get(f"{API_URL}/scene/intro")
        response.raise_for_status()
        data = response.json()
        
        # Check if the image URL is a placeholder or a real generated image
        if "placehold.co" in data['image_url']:
            print("⚠️ Image generation not working - using placeholder image")
            return False
        else:
            print("✅ Image generation working!")
            print(f"Generated image URL: {data['image_url']}")
            return True
    except Exception as e:
        print(f"❌ Image generation test failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test RPG Maestro API components")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--scene", action="store_true", help="Test scene endpoint")
    parser.add_argument("--objectives", action="store_true", help="Test objectives endpoint")
    parser.add_argument("--action", action="store_true", help="Test action endpoint")
    parser.add_argument("--image", action="store_true", help="Test image generation")
    
    args = parser.parse_args()
    
    # If no specific tests are specified, run all tests
    if not (args.all or args.scene or args.objectives or args.action or args.image):
        args.all = True
    
    results = {}
    
    if args.all or args.scene:
        results["scene"] = test_scene_endpoint()
    
    if args.all or args.objectives:
        results["objectives"] = test_objectives_endpoint()
    
    if args.all or args.action:
        results["action"] = test_action_endpoint()
    
    if args.all or args.image:
        results["image"] = test_image_generation()
    
    # Print summary
    print("\n===== Test Summary =====")
    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test.capitalize()}: {status}")
    
    # Return non-zero exit code if any test failed
    if not all(results.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
