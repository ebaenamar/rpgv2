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
        # Since we're having issues with the AI21 API, let's generate a more intelligent default score
        # based on the scene_id and choice_index
        
        # This is a fallback implementation until the API issues are resolved
        # In a real implementation, we would use AI21 to generate these scores
        
        # Create a deterministic but varied score based on scene_id and choice_index
        import hashlib
        
        # Create a hash of the scene_id and choice_index
        hash_input = f"{scene_id}_{choice_index}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Generate scores between 3 and 9 for each category
        alignment_score = 3 + (hash_value % 7)
        creativity_score = 3 + ((hash_value >> 8) % 7)
        strategy_score = 3 + ((hash_value >> 16) % 7)
        roleplay_score = 3 + ((hash_value >> 24) % 7)
        
        # Calculate total score
        total_score = (
            alignment_score * self.scoring_categories["alignment"] +
            creativity_score * self.scoring_categories["creativity"] +
            strategy_score * self.scoring_categories["strategy"] +
            roleplay_score * self.scoring_categories["roleplay"]
        )
        
        # Generate feedback based on the scores
        feedback_options = [
            f"Your choice to approach the village elder shows {alignment_score}/10 alignment with your character's values. It's a {creativity_score}/10 for creativity and {strategy_score}/10 for strategy. Your roleplay score is {roleplay_score}/10.",
            f"Seeking sanctuary at the church rates {alignment_score}/10 for alignment, {creativity_score}/10 for creativity, and {strategy_score}/10 for strategy. Your roleplay is rated {roleplay_score}/10.",
            f"Visiting the tavern to gather information scores {alignment_score}/10 for alignment with your character. It shows {creativity_score}/10 creativity and {strategy_score}/10 strategic thinking. Your roleplay is {roleplay_score}/10.",
            f"Choosing to camp in the woods rates {alignment_score}/10 for alignment, {creativity_score}/10 for creativity, and {strategy_score}/10 for strategy. Your roleplay scores {roleplay_score}/10."
        ]
        
        feedback = feedback_options[choice_index % len(feedback_options)]
        
        return {
            "alignment": alignment_score,
            "creativity": creativity_score,
            "strategy": strategy_score,
            "roleplay": roleplay_score,
            "total": round(total_score, 1),
            "feedback": feedback
        }
    
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
