#!/usr/bin/env python

import requests
import time
import sys
import json

# Configuration
API_URL = "http://localhost:8080"
MAX_RETRIES = 10
RETRY_DELAY = 2  # seconds

def test_api_connection():
    """Test basic connection to the API"""
    print("Testing connection to API...")
    
    for i in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_URL}/")
            if response.status_code == 200:
                print("✅ Connection successful!")
                return True
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"Waiting for API to start... (attempt {i+1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    
    print("❌ Could not connect to API after multiple attempts")
    return False

def test_scene_endpoint():
    """Test the scene endpoint"""
    print("\nTesting scene endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/api/scene/intro")
        if response.status_code == 200:
            data = response.json()
            if 'scene' in data and 'choices' in data:
                print("✅ Scene endpoint working!")
                print(f"Scene description: {data['scene']['description'][:50]}...")
                print(f"Number of choices: {len(data['choices'])}")
                return True
            else:
                print("❌ Scene endpoint returned unexpected data structure")
                return False
        else:
            print(f"❌ Scene endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing scene endpoint: {e}")
        return False

def test_action_endpoint():
    """Test the action endpoint"""
    print("\nTesting action endpoint...")
    
    try:
        payload = {
            "scene_id": "intro",
            "choice_index": 0
        }
        response = requests.post(f"{API_URL}/api/action", json=payload)
        if response.status_code == 200:
            data = response.json()
            if 'agent_response' in data and 'next_scene_id' in data:
                print("✅ Action endpoint working!")
                print(f"Agent response: {data['agent_response'][:50]}...")
                print(f"Next scene: {data['next_scene_id']}")
                return True
            else:
                print("❌ Action endpoint returned unexpected data structure")
                return False
        else:
            print(f"❌ Action endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing action endpoint: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall success"""
    print("=== RPG Maestro Docker API Tests ===\n")
    
    connection_success = test_api_connection()
    if not connection_success:
        return False
    
    scene_success = test_scene_endpoint()
    action_success = test_action_endpoint()
    
    print("\n=== Test Summary ===")
    print(f"API Connection: {'✅' if connection_success else '❌'}")
    print(f"Scene Endpoint: {'✅' if scene_success else '❌'}")
    print(f"Action Endpoint: {'✅' if action_success else '❌'}")
    
    overall_success = connection_success and scene_success and action_success
    print(f"\nOverall Test Result: {'✅ PASSED' if overall_success else '❌ FAILED'}")
    
    return overall_success

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
