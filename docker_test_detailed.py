#!/usr/bin/env python

import requests
import time
import sys
import json
import subprocess
import os

# Configuration
API_URL = "http://localhost:8080"
MAX_RETRIES = 15
RETRY_DELAY = 2  # seconds

def run_command(command):
    """Run a shell command and return the output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    return {
        "exit_code": process.returncode,
        "stdout": stdout,
        "stderr": stderr
    }

def check_docker_container():
    """Check if the Docker container is running and get logs if it's not"""
    print("Checking Docker container status...")
    
    result = run_command("docker ps | grep rpg-maestro-api-test")
    if result["exit_code"] != 0 or "rpg-maestro-api-test" not in result["stdout"]:
        print("\n\033[91mContainer is not running! Checking logs...\033[0m")
        logs = run_command("docker logs rpg-maestro-api-test 2>&1 || echo 'No logs available'")
        print("\n\033[93mContainer logs:\033[0m")
        print(logs["stdout"])
        return False
    
    print("\033[92m✓ Container is running!\033[0m")
    return True

def test_api_connection():
    """Test basic connection to the API"""
    print("\nTesting connection to API...")
    
    for i in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_URL}/")
            if response.status_code == 200:
                print(f"\033[92m✓ Connection successful! Response: {response.json()}\033[0m")
                return True
            else:
                print(f"\033[91m✗ Unexpected status code: {response.status_code}\033[0m")
                print(f"Response: {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"Waiting for API to start... (attempt {i+1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    
    print("\033[91m✗ Could not connect to API after multiple attempts\033[0m")
    return False

def test_scene_endpoint():
    """Test the scene endpoint"""
    print("\nTesting scene endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/api/scene/intro")
        if response.status_code == 200:
            data = response.json()
            if 'scene' in data and 'choices' in data:
                print("\033[92m✓ Scene endpoint working!\033[0m")
                print(f"Scene description: {data['scene']['description'][:50]}...")
                print(f"Number of choices: {len(data['choices'])}")
                return True
            else:
                print("\033[91m✗ Scene endpoint returned unexpected data structure\033[0m")
                print(f"Response: {json.dumps(data, indent=2)}")
                return False
        else:
            print(f"\033[91m✗ Scene endpoint returned status code: {response.status_code}\033[0m")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"\033[91m✗ Error testing scene endpoint: {e}\033[0m")
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
                print("\033[92m✓ Action endpoint working!\033[0m")
                print(f"Agent response: {data['agent_response'][:50]}...")
                print(f"Next scene: {data['next_scene_id']}")
                return True
            else:
                print("\033[91m✗ Action endpoint returned unexpected data structure\033[0m")
                print(f"Response: {json.dumps(data, indent=2)}")
                return False
        else:
            print(f"\033[91m✗ Action endpoint returned status code: {response.status_code}\033[0m")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"\033[91m✗ Error testing action endpoint: {e}\033[0m")
        return False

def check_api_logs():
    """Get the logs from the Docker container"""
    print("\nFetching container logs...")
    logs = run_command("docker logs rpg-maestro-api-test 2>&1 | tail -n 50")
    print("\n\033[93mLast 50 lines of container logs:\033[0m")
    print(logs["stdout"])

def run_all_tests():
    """Run all tests and return overall success"""
    print("=== RPG Maestro Docker API Tests ===\n")
    
    # Check if container is running
    container_running = check_docker_container()
    if not container_running:
        return False
    
    # Test API connection
    connection_success = test_api_connection()
    if not connection_success:
        check_api_logs()
        return False
    
    # Test endpoints
    scene_success = test_scene_endpoint()
    action_success = test_action_endpoint()
    
    # Print test summary
    print("\n=== Test Summary ===")
    print(f"Docker Container: {'\033[92m✓' if container_running else '\033[91m✗'}\033[0m")
    print(f"API Connection: {'\033[92m✓' if connection_success else '\033[91m✗'}\033[0m")
    print(f"Scene Endpoint: {'\033[92m✓' if scene_success else '\033[91m✗'}\033[0m")
    print(f"Action Endpoint: {'\033[92m✓' if action_success else '\033[91m✗'}\033[0m")
    
    overall_success = container_running and connection_success and scene_success and action_success
    print(f"\nOverall Test Result: {'\033[92m✓ PASSED' if overall_success else '\033[91m✗ FAILED'}\033[0m")
    
    if not overall_success:
        check_api_logs()
    
    return overall_success

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
