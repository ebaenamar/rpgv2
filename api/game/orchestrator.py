from ai21 import AI21Client
import json
import os
from typing import List, Dict, Any

class GameOrchestrator:
    def __init__(self, api_key):
        self.client = AI21Client(api_key=api_key)
        self.current_scene = None
        self.player_state = {
            "alignment": {
                "law_chaos": 0,  # -100 (chaotic) to 100 (lawful)
                "good_evil": 0,  # -100 (evil) to 100 (good)
            },
            "skills": {},
            "experience": 0,
        }
        self.agent_state = {
            "trust": 50,  # 0-100
            "recent_actions": [],
        }
        
        # Load scenes from JSON file
        self.scenes = self._load_scenes()
        
    def _load_scenes(self) -> Dict[str, Any]:
        """Load scene data from JSON file"""
        # For now, return a hardcoded scene for testing
        return {
            "intro": {
                "scene_id": "intro",
                "description": "You stand at the edge of a medieval village. The church bell tower looms in the distance, and villagers hurry about their daily tasks. Ser Elyen, your companion, stands beside you, his weathered armor gleaming in the afternoon sun.",
                "rag_context_query": "medieval English village, 13th century, daily life",
                "region": "England",
                "actions": [
                    "A) Approach the village elder to inquire about lodging.",
                    "B) Head directly to the church to seek sanctuary.",
                    "C) Visit the local tavern to gather information.",
                    "D) Remain outside the village and make camp in the woods."
                ],
                "next_scene_map": {
                    "A": "village_elder",
                    "B": "church",
                    "C": "tavern",
                    "D": "forest_camp"
                }
            },
            "village_elder": {
                "scene_id": "village_elder",
                "description": "The village elder, a man with a long gray beard and weathered hands, greets you with suspicion. His small cottage is filled with herbs and scrolls, suggesting he is both the leader and healer of this community.",
                "rag_context_query": "medieval village elder, healer, community leader, 13th century England",
                "region": "England",
                "actions": [
                    "A) Offer payment for a night's lodging in the village.",
                    "B) Mention that you are on a quest and need information.",
                    "C) Intimidate the elder into helping you.",
                    "D) Show him a mysterious symbol you carry."
                ],
                "next_scene_map": {
                    "A": "lodging",
                    "B": "quest_info",
                    "C": "intimidation",
                    "D": "symbol_reveal"
                }
            },
            # Add more scenes as needed
        }
        
    def get_scene(self, scene_id: str) -> Dict[str, Any]:
        """Get scene data by ID"""
        if scene_id not in self.scenes:
            raise ValueError(f"Scene {scene_id} not found")
            
        self.current_scene = scene_id
        return self.scenes[scene_id]
        
    def generate_scene_choices(self, scene_context: str, historical_context: List[Dict[str, str]]) -> List[str]:
        """Generate player choices for the current scene using Maestro"""
        # Extract historical facts as text
        historical_facts = "\n".join([f"- {item['text']}" for item in historical_context])
        
        # If we already have predefined choices, return those
        if self.current_scene and "actions" in self.scenes[self.current_scene]:
            return self.scenes[self.current_scene]["actions"]
            
        # Otherwise, generate choices with Maestro
        try:
            run_result = self.client.beta.maestro.runs.create_and_poll(
                input=f"Generate 4 player choices for this medieval RPG scene:\n\nScene: {scene_context}\n\nHistorical context:\n{historical_facts}",
                requirements=[
                    {
                        "name": "choice_count",
                        "description": "Generate exactly 4 distinct choices labeled A, B, C, and D",
                        "is_mandatory": True
                    },
                    {
                        "name": "historical_accuracy",
                        "description": f"Choices must be historically plausible based on the provided historical context",
                        "is_mandatory": True
                    },
                    {
                        "name": "moral_diversity",
                        "description": "Choices should represent different moral alignments (good/evil, lawful/chaotic)",
                        "is_mandatory": True
                    }
                ]
            )
            
            # Parse the choices from the output
            choices = run_result.output.split("\n")
            # Filter out any non-choice lines
            choices = [c for c in choices if c.startswith("A)") or c.startswith("B)") or 
                      c.startswith("C)") or c.startswith("D)")]
            
            # Ensure we have exactly 4 choices
            if len(choices) != 4:
                # Fall back to default choices
                choices = [
                    "A) Proceed cautiously forward.",
                    "B) Speak with your companion about the situation.",
                    "C) Look for an alternative path.",
                    "D) Rest and consider your options."
                ]
                
            return choices
            
        except Exception as e:
            print(f"Error generating choices: {e}")
            # Fall back to default choices
            return [
                "A) Proceed cautiously forward.",
                "B) Speak with your companion about the situation.",
                "C) Look for an alternative path.",
                "D) Rest and consider your options."
            ]
    
    def update_player_state(self, scene_id: str, choice_index: int) -> None:
        """Update player state based on their choice"""
        # Define the impact of choices on alignment and trust
        # This would be more sophisticated in a full implementation
        choice_impacts = {
            "intro": [
                {"law_chaos": 5, "good_evil": 0, "trust": 0},  # A - lawful neutral
                {"law_chaos": 10, "good_evil": 5, "trust": 5},  # B - lawful good
                {"law_chaos": -5, "good_evil": 0, "trust": 0},  # C - chaotic neutral
                {"law_chaos": -10, "good_evil": 0, "trust": -5}   # D - chaotic neutral
            ],
            "village_elder": [
                {"law_chaos": 5, "good_evil": 0, "trust": 0},  # A - lawful neutral
                {"law_chaos": 0, "good_evil": 5, "trust": 5},  # B - neutral good
                {"law_chaos": -5, "good_evil": -10, "trust": -10},  # C - chaotic evil
                {"law_chaos": 0, "good_evil": 0, "trust": 0}   # D - true neutral
            ],
            # Add more scenes as needed
        }
        
        # Apply the impact if defined
        if scene_id in choice_impacts and 0 <= choice_index < len(choice_impacts[scene_id]):
            impact = choice_impacts[scene_id][choice_index]
            
            # Update alignment
            self.player_state["alignment"]["law_chaos"] += impact["law_chaos"]
            self.player_state["alignment"]["law_chaos"] = max(-100, min(100, self.player_state["alignment"]["law_chaos"]))
            
            self.player_state["alignment"]["good_evil"] += impact["good_evil"]
            self.player_state["alignment"]["good_evil"] = max(-100, min(100, self.player_state["alignment"]["good_evil"]))
            
            # Update agent trust
            self.agent_state["trust"] += impact["trust"]
            self.agent_state["trust"] = max(0, min(100, self.agent_state["trust"]))
            
            # Add to recent actions
            choice_letter = "ABCD"[choice_index]
            scene = self.scenes[scene_id]
            action = scene["actions"][choice_index]
            self.agent_state["recent_actions"].append(action)
            
            # Keep only the 5 most recent actions
            if len(self.agent_state["recent_actions"]) > 5:
                self.agent_state["recent_actions"] = self.agent_state["recent_actions"][-5:]
                
        # Award experience
        self.player_state["experience"] += 10
