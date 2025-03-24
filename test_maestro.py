#!/usr/bin/env python3

import os
import json
import sys
from dotenv import load_dotenv
from api.game.agent import MaestroCharacterAgent
from api.game.orchestrator import GameOrchestrator

# Load environment variables
load_dotenv('.env.docker')

# Get API keys from environment
AI21_API_KEY = os.getenv('AI21_API_KEY')
if not AI21_API_KEY:
    print("Error: AI21_API_KEY not found in environment variables")
    sys.exit(1)

def test_maestro_character_agent():
    """Test the MaestroCharacterAgent with Maestro API"""
    print("\n=== Testing MaestroCharacterAgent with Maestro API ===")
    
    # Create a character profile
    character_profile = {
        "name": "Ser Elyen",
        "role": "Knight Companion",
        "alignment": "Lawful Good",
        "background": "A veteran knight who has served in the Crusades and now seeks redemption for past sins.",
        "personality": "Honorable, stoic, protective, and occasionally haunted by memories of war."
    }
    
    # Create the agent
    agent = MaestroCharacterAgent(character_profile, AI21_API_KEY)
    
    # Test scene context and player action
    scene_context = "You stand at the edge of a medieval village. The church bell tower looms in the distance."
    player_action = "I suggest we approach the village elder to inquire about lodging."
    
    # Create historical context
    historical_context = [
        {"text": "In 13th century England, travelers often sought permission from village elders before staying."},
        {"text": "Knights were expected to uphold a code of chivalry, including protecting the weak."}
    ]
    
    # Generate response
    print("Generating character response...")
    response = agent.generate_response(scene_context, player_action, historical_context)
    print(f"\nCharacter Response:\n{response}\n")
    
    return response is not None

def test_maestro_scene_choices():
    """Test the GameOrchestrator scene choices generation with Maestro API"""
    print("\n=== Testing GameOrchestrator Scene Choices with Maestro API ===")
    
    # Create the orchestrator
    orchestrator = GameOrchestrator(AI21_API_KEY)
    
    # Test scene context
    scene_context = "You've arrived at a crossroads outside a small medieval town. A storm is brewing in the distance."
    
    # Create historical context
    historical_context = [
        {"text": "Medieval travelers often sought shelter in monasteries during storms."},
        {"text": "Bandits were known to prey on travelers at crossroads in medieval England."}
    ]
    
    # Generate choices
    print("Generating scene choices...")
    choices = orchestrator.generate_scene_choices(scene_context, historical_context)
    
    print("\nGenerated Choices:")
    for choice in choices:
        print(f"- {choice}")
    print()
    
    return len(choices) == 4

def test_end_to_end_flow():
    """Test the end-to-end game flow with Maestro"""
    print("\n=== Testing End-to-End Game Flow with Maestro ===")
    
    # Create the orchestrator and agent
    orchestrator = GameOrchestrator(AI21_API_KEY)
    
    character_profile = {
        "name": "Ser Elyen",
        "role": "Knight Companion",
        "alignment": "Lawful Good",
        "background": "A veteran knight who has served in the Crusades and now seeks redemption for past sins.",
        "personality": "Honorable, stoic, protective, and occasionally haunted by memories of war."
    }
    
    agent = MaestroCharacterAgent(character_profile, AI21_API_KEY)
    
    # Get the intro scene
    scene = orchestrator.get_scene("intro")
    print(f"Scene: {scene['scene_id']}")
    print(f"Description: {scene['description']}")
    
    # Display choices
    print("\nChoices:")
    for action in scene['actions']:
        print(f"- {action}")
    
    # Simulate player choice (choose option A)
    choice_index = 0  # Option A
    choice = scene['actions'][choice_index]
    print(f"\nPlayer chooses: {choice}")
    
    # Update player state
    orchestrator.update_player_state(scene['scene_id'], choice_index)
    
    # Get next scene based on choice
    next_scene_id = scene['next_scene_map']['A']
    next_scene = orchestrator.get_scene(next_scene_id)
    
    print(f"\nNext Scene: {next_scene['scene_id']}")
    print(f"Description: {next_scene['description']}")
    
    # Generate character response to the player's choice
    historical_context = [
        {"text": "In 13th century England, travelers often sought permission from village elders before staying."},
        {"text": "Knights were expected to uphold a code of chivalry, including protecting the weak."}
    ]
    
    response = agent.generate_response(
        scene['description'],
        choice,
        historical_context
    )
    
    print(f"\nCharacter Response:\n{response}\n")
    
    # Display choices for the next scene
    print("\nChoices for next scene:")
    for action in next_scene['actions']:
        print(f"- {action}")
    
    return True

def main():
    """Run all tests"""
    print("Starting Maestro Integration Tests")
    
    # Run tests
    character_test = test_maestro_character_agent()
    choices_test = test_maestro_scene_choices()
    flow_test = test_end_to_end_flow()
    
    # Print results
    print("\n=== Test Results ===")
    print(f"Character Agent Test: {'PASSED' if character_test else 'FAILED'}")
    print(f"Scene Choices Test: {'PASSED' if choices_test else 'FAILED'}")
    print(f"End-to-End Flow Test: {'PASSED' if flow_test else 'FAILED'}")
    
    # Overall result
    if character_test and choices_test and flow_test:
        print("\nAll Maestro tests PASSED!")
        return 0
    else:
        print("\nSome tests FAILED. See details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
