from ai21 import AI21Client
from typing import List, Dict, Any

class MaestroCharacterAgent:
    def __init__(self, character_profile: Dict[str, Any], api_key: str):
        self.client = AI21Client(api_key=api_key)
        self.character_profile = character_profile
        self.memory = {
            "name": character_profile["name"],
            "alignment": character_profile["alignment"],
            "trust_in_player": 50,
            "recent_actions": [],
            "mood": "neutral"
        }
        
    def _format_prompt(self, scene_context: str, player_action: str, historical_context: List[Dict[str, Any]]) -> str:
        """Format the prompt for the LLM with all context"""
        # Extract historical facts
        historical_facts = "\n".join([f"- {item['text']}" for item in historical_context])
        
        # Format recent actions
        recent_actions = "\n".join([f"- {action}" for action in self.memory["recent_actions"]])
        if not recent_actions:
            recent_actions = "- This is your first interaction with the player."
        
        # Determine mood description based on trust level
        trust_level = self.memory["trust_in_player"]
        if trust_level >= 80:
            mood_description = "very trusting and friendly"
        elif trust_level >= 60:
            mood_description = "generally trusting"
        elif trust_level >= 40:
            mood_description = "neutral"
        elif trust_level >= 20:
            mood_description = "somewhat suspicious"
        else:
            mood_description = "distrustful and guarded"
        
        self.memory["mood"] = mood_description.split()[0]  # Set the first word as the mood
        
        # Construct the full prompt
        prompt = f"""You are {self.character_profile['name']}, a {self.character_profile['alignment']} character in a medieval RPG set in 13th century England.

Your background: {self.character_profile.get('background', 'A mysterious figure with a complex past.')}

Current scene: {scene_context}

The player has just chosen to: {player_action}

Historical context (use these facts in your response):
{historical_facts}

Recent player actions:
{recent_actions}

Your current relationship with the player: You are {mood_description} toward the player.

Respond as {self.character_profile['name']}, providing your reaction to the player's choice. Your response should be in first person, show your personality, and incorporate the historical context. Keep your response to 2-3 sentences."""
        
        return prompt
        
    def generate_response(self, scene_context: str, player_action: str, historical_context: List[Dict[str, Any]]) -> str:
        """Generate a character response using Maestro with requirements"""
        # Format prompt with all context
        prompt = self._format_prompt(scene_context, player_action, historical_context)
        
        try:
            # Generate response with Maestro requirements
            run_result = self.client.beta.maestro.runs.create_and_poll(
                input=prompt,
                requirements=[
                    {
                        "name": "character_consistency",
                        "description": f"Response must be consistent with character profile: {self.character_profile['name']}, a {self.character_profile['alignment']} character",
                        "is_mandatory": True
                    },
                    {
                        "name": "historical_accuracy",
                        "description": "Response must incorporate at least one historical fact from the provided historical context",
                        "is_mandatory": True
                    },
                    {
                        "name": "emotional_response",
                        "description": f"Response should reflect character's current mood: {self.memory['mood']}",
                        "is_mandatory": True
                    },
                    {
                        "name": "first_person",
                        "description": "Response must be in first person as if the character is speaking directly",
                        "is_mandatory": True
                    },
                    {
                        "name": "length",
                        "description": "Response should be 2-3 sentences long",
                        "is_mandatory": True
                    }
                ]
            )
            
            return run_result.output
            
        except Exception as e:
            print(f"Error generating character response: {e}")
            # Fallback response if Maestro fails
            trust_level = self.memory["trust_in_player"]
            if trust_level >= 60:
                return f"I think that's a wise choice. Let us proceed carefully."
            elif trust_level >= 30:
                return f"Very well. I shall follow your lead, though I have my reservations."
            else:
                return f"I question your judgment, but I will accompany you nonetheless."
                
    def update_memory(self, player_action: str, trust_change: int) -> None:
        """Update the agent's memory based on player actions"""
        # Add to recent actions
        self.memory["recent_actions"].append(player_action)
        
        # Keep only the 5 most recent actions
        if len(self.memory["recent_actions"]) > 5:
            self.memory["recent_actions"] = self.memory["recent_actions"][-5:]
            
        # Update trust level
        self.memory["trust_in_player"] += trust_change
        self.memory["trust_in_player"] = max(0, min(100, self.memory["trust_in_player"]))
        
        # Update mood based on trust level
        trust_level = self.memory["trust_in_player"]
        if trust_level >= 80:
            self.memory["mood"] = "trusting"
        elif trust_level >= 60:
            self.memory["mood"] = "friendly"
        elif trust_level >= 40:
            self.memory["mood"] = "neutral"
        elif trust_level >= 20:
            self.memory["mood"] = "suspicious"
        else:
            self.memory["mood"] = "distrustful"
