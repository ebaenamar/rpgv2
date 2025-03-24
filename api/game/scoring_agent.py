import ai21
from typing import Dict, Any, List

class ScoringAgent:
    """
    Agent responsible for scoring player choices and providing feedback
    based on game objectives and player alignment.
    """
    
    def __init__(self, api_key: str):
        # Initialize the AI21 client with the API key
        self.client = ai21.AI21Client(api_key=api_key)
        
        # Define scoring categories and weights
        self.scoring_categories = {
            "alignment": 0.3,  # How well the choice aligns with character's moral compass
            "creativity": 0.2,  # How creative or unexpected the choice is
            "strategy": 0.3,  # How strategically sound the choice is
            "roleplay": 0.2,  # How well the choice fits the character's persona
        }
        
        # Game objectives that will be explained to the player
        self.game_objectives = [
            "Navigate the medieval world while making choices that align with your character's moral compass",
            "Build relationships with NPCs to gain allies and information",
            "Discover the truth behind the mysterious events in the kingdom",
            "Develop your character's skills and abilities through your choices",
            "Balance your character's alignment between good/evil and lawful/chaotic"
        ]
    
    def get_game_objectives(self) -> List[str]:
        """Return the list of game objectives to display to the player"""
        return self.game_objectives
    
    def score_choice(self, scene_id: str, choice_index: int, player_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a player's choice based on the scene, choice, and current player state.
        Returns a dictionary with scores and feedback.
        """
        try:
            # Prepare the context for scoring
            context = self._prepare_scoring_context(scene_id, choice_index, player_state)
            
            # Use Maestro to evaluate the choice
            run_result = self.client.beta.maestro.runs.create_and_poll(
                input=context,
                requirements=[
                    {
                        "name": "scoring_format",
                        "description": "The response must be in JSON format with scores for each category (alignment, creativity, strategy, roleplay) on a scale of 1-10, and a 'feedback' field with constructive feedback about the choice.",
                        "is_mandatory": True
                    },
                    {
                        "name": "balanced_scoring",
                        "description": "Scores should be balanced and realistic, not all 10s or all 1s. Consider the context of the choice and the player's current state.",
                        "is_mandatory": True
                    },
                    {
                        "name": "helpful_feedback",
                        "description": "Feedback should be constructive, specific to the choice made, and offer insights about consequences or alternative approaches.",
                        "is_mandatory": True
                    }
                ]
            )
            
            # Parse the result
            try:
                # The result is expected to be in JSON format
                import json
                scores = json.loads(run_result.result)
                
                # Calculate the weighted total score
                total_score = 0
                for category, weight in self.scoring_categories.items():
                    if category in scores:
                        total_score += scores[category] * weight
                
                # Add the total score to the result
                scores["total"] = round(total_score, 1)
                
                return scores
            except json.JSONDecodeError:
                # If the result is not valid JSON, return a default score
                return self._generate_default_score("Could not parse scoring result")
                
        except Exception as e:
            print(f"Error scoring choice: {e}")
            return self._generate_default_score(f"Error: {str(e)}")
    
    def _prepare_scoring_context(self, scene_id: str, choice_index: int, player_state: Dict[str, Any]) -> str:
        """
        Prepare the context for the scoring agent to evaluate the choice.
        """
        # Format the player state information
        alignment_info = f"Law/Chaos: {player_state.get('alignment', {}).get('law_chaos', 0)}, "
        alignment_info += f"Good/Evil: {player_state.get('alignment', {}).get('good_evil', 0)}"
        
        skills_info = ", ".join([f"{k}: {v}" for k, v in player_state.get('skills', {}).items()])
        if not skills_info:
            skills_info = "No skills developed yet"
        
        # Construct the context
        context = f"""Scene ID: {scene_id}
        Choice Index: {choice_index}
        Player Alignment: {alignment_info}
        Player Skills: {skills_info}
        Experience Points: {player_state.get('experience', 0)}
        
        Task: Score this player choice based on alignment with character, creativity, strategic value, and roleplay quality.
        Provide scores on a scale of 1-10 for each category and constructive feedback.
        Format the response as a JSON object with keys: alignment, creativity, strategy, roleplay, and feedback."""
        
        return context
    
    def _generate_default_score(self, error_message: str) -> Dict[str, Any]:
        """
        Generate a default score when scoring fails.
        """
        return {
            "alignment": 5,
            "creativity": 5,
            "strategy": 5,
            "roleplay": 5,
            "total": 5,
            "feedback": f"Default score generated. {error_message}"
        }
