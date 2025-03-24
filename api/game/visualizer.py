import os
import replicate
from typing import Optional

class SceneVisualizer:
    def __init__(self, api_key: str):
        # Set the Replicate API token
        os.environ['REPLICATE_API_TOKEN'] = api_key
        
    def generate_scene_image(self, scene_description: str, historical_context: str = "") -> str:
        """Generate an image for the current scene using Replicate"""
        try:
            # Combine scene description with historical details for accuracy
            prompt = f"Medieval scene: {scene_description}"
            if historical_context:
                prompt += f" Historical details: {historical_context}"
                
            # Make the request to the Replicate model
            output = replicate.run(
                "sundai-club/handala_model_1:bcbb4661012269b7fc3e5effc65b82283452c795c8e3195e45ddd35672f0c4ec",
                input={
                    "model": "dev",
                    "go_fast": False,
                    "lora_scale": 1,
                    "megapixels": "1",
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "guidance_scale": 3,
                    "output_quality": 80,
                    "prompt_strength": 0.8,
                    "extra_lora_scale": 1,
                    "num_inference_steps": 28,
                    "prompt": prompt
                }
            )
            
            # Return the URL of the generated image
            if isinstance(output, list) and len(output) > 0:
                return output[0]
            elif isinstance(output, str):
                return output
            else:
                print(f"Unexpected output format from Replicate: {type(output)}")
                return self._get_fallback_image()
                
        except Exception as e:
            print(f"Error generating scene image: {e}")
            return self._get_fallback_image()
            
    def _get_fallback_image(self) -> str:
        """Return a fallback image URL if image generation fails"""
        # In a production system, you would have a set of fallback images
        return "https://placehold.co/600x400?text=Scene+Image+Unavailable"
