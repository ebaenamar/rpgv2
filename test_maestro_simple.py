#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.docker')

# Get API keys from environment
AI21_API_KEY = os.getenv('AI21_API_KEY')
if not AI21_API_KEY:
    print("Error: AI21_API_KEY not found in environment variables")
    sys.exit(1)

def test_maestro_api():
    """Test the Maestro API directly"""
    print("\n=== Testing Maestro API ===")
    
    try:
        # Import AI21 here to avoid dependency issues
        import ai21
        
        # Print the AI21 version
        print(f"AI21 SDK Version: {ai21.__version__}")
        
        # Initialize the AI21 client
        client = ai21.AI21Client(api_key=AI21_API_KEY)
        
        # Test if Maestro is available
        has_maestro = hasattr(client, 'beta') and hasattr(client.beta, 'maestro')
        print(f"Maestro API Available: {has_maestro}")
        
        if has_maestro:
            # Test a simple Maestro request
            try:
                print("Testing Maestro with a simple request...")
                run_result = client.beta.maestro.runs.create_and_poll(
                    input="Write a short poem about a medieval knight",
                    requirements=[
                        {
                            "name": "length",
                            "description": "The poem should be less than 100 characters",
                            "is_mandatory": True
                        },
                        {
                            "name": "rhyme",
                            "description": "The poem should rhyme",
                            "is_mandatory": True
                        }
                    ]
                )
                # Print the full run_result to understand its structure
                print("\nMaestro Response Structure:")
                print(f"Response type: {type(run_result)}")
                print(f"Available attributes: {dir(run_result)}")
                
                # Try to access the response content in different ways
                if hasattr(run_result, 'result'):
                    print(f"\nMaestro Result:\n{run_result.result}\n")
                elif hasattr(run_result, 'content'):
                    print(f"\nMaestro Content:\n{run_result.content}\n")
                elif hasattr(run_result, 'text'):
                    print(f"\nMaestro Text:\n{run_result.text}\n")
                elif hasattr(run_result, 'response'):
                    print(f"\nMaestro Response:\n{run_result.response}\n")
                else:
                    print(f"\nRaw Maestro Response:\n{run_result}\n")
                return True
            except Exception as e:
                print(f"Error testing Maestro: {e}")
                return False
        else:
            print("Maestro API is not available in this version of the AI21 SDK.")
            print("Please upgrade to a newer version that supports Maestro.")
            return False
    except ImportError:
        print("Error: AI21 package not installed. Please install it with 'pip install ai21'.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Run the Maestro API test"""
    print("Starting Maestro API Test")
    
    # Run test
    maestro_test = test_maestro_api()
    
    # Print results
    print("\n=== Test Results ===")
    print(f"Maestro API Test: {'PASSED' if maestro_test else 'FAILED'}")
    
    # Overall result
    if maestro_test:
        print("\nMaestro API test PASSED!")
        return 0
    else:
        print("\nMaestro API test FAILED. See details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
