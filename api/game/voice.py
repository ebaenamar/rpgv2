import requests
import base64
import os
import json
from typing import Optional

class SesameVoice:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.sesame.ai/v1/speech"
        # Create directory for audio files
        os.makedirs("static/audio", exist_ok=True)
        
    def text_to_speech(self, text: str, voice_id: str = "maya", emotion: str = "neutral") -> str:
        """Convert text to speech using Sesame Maya"""
        try:
            # Map our mood to Sesame emotions
            emotion_mapping = {
                "trusting": "happy",
                "friendly": "happy",
                "neutral": "neutral",
                "suspicious": "serious",
                "distrustful": "angry"
            }
            
            # Use mapped emotion or fallback to neutral
            mapped_emotion = emotion_mapping.get(emotion, "neutral")
            
            # Make API request to Sesame
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "voice_id": voice_id,
                    "emotion": mapped_emotion
                }
            )
            
            # Check for successful response
            if response.status_code == 200:
                # Save audio file
                audio_data = base64.b64decode(response.json()["audio"])
                file_name = f"{voice_id}_{hash(text)}.mp3"
                file_path = f"static/audio/{file_name}"
                
                with open(file_path, "wb") as f:
                    f.write(audio_data)
                    
                return f"/static/audio/{file_name}"
            else:
                print(f"Error from Sesame API: {response.status_code} - {response.text}")
                return self._get_fallback_audio()
                
        except Exception as e:
            print(f"Error generating speech: {e}")
            return self._get_fallback_audio()
            
    def _get_fallback_audio(self) -> str:
        """Return a fallback audio URL if speech generation fails"""
        # In a production system, you would have a set of fallback audio files
        return "/static/audio/fallback.mp3"
