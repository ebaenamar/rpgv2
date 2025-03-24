from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn

# Import our game components
from game.orchestrator import GameOrchestrator
from game.rag import RAGRetriever
from game.agent import MaestroCharacterAgent
from game.visualizer import SceneVisualizer
from game.voice import SesameVoice

load_dotenv()

app = FastAPI(title="RPG Maestro API", description="API for the AI21 Maestro-powered RPG game")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = None
rag = None
agent = None
visualizer = None
voice = None

@app.on_event("startup")
async def startup_event():
    global orchestrator, rag, agent, visualizer, voice
    
    # Initialize components
    orchestrator = GameOrchestrator(api_key=os.getenv("AI21_API_KEY"))
    rag = RAGRetriever(
        index_path="data/faiss_index",
        documents_path="data/historical_documents.json"
    )
    agent = MaestroCharacterAgent(
        character_profile={
            "name": "Ser Elyen",
            "alignment": "Neutral Good",
            "background": "A fallen knight seeking redemption"
        },
        api_key=os.getenv("AI21_API_KEY")
    )
    visualizer = SceneVisualizer(api_key=os.getenv("REPLICATE_API_TOKEN"))
    voice = SesameVoice(api_key=os.getenv("SESAME_API_KEY"))

# Game state
game_state = {}

class ActionRequest(BaseModel):
    scene_id: str
    choice_index: int

@app.get("/")
async def root():
    return {"message": "Welcome to RPG Maestro API"}

@app.get("/api/scene/{scene_id}")
async def get_scene(scene_id: str):
    # Get scene data
    scene = orchestrator.get_scene(scene_id)
    
    # Get historical context from RAG
    historical_context = rag.retrieve(
        query=scene["rag_context_query"],
        filters={"region": scene.get("region", None)}
    )
    
    # Generate choices using Maestro
    choices = orchestrator.generate_scene_choices(
        scene_context=scene["description"],
        historical_context=historical_context
    )
    
    # Generate scene image
    image_url = visualizer.generate_scene_image(
        scene_description=scene["description"],
        historical_context=historical_context[0]["text"] if historical_context else ""
    )
    
    return {
        "scene": scene,
        "choices": choices,
        "image_url": image_url
    }

@app.post("/api/action")
async def process_action(request: ActionRequest):
    # Get scene and player choice
    scene = orchestrator.get_scene(request.scene_id)
    choice = scene["actions"][request.choice_index]
    
    # Get historical context from RAG
    historical_context = rag.retrieve(
        query=scene["rag_context_query"],
        filters={"region": scene.get("region", None)}
    )
    
    # Update player state based on choice
    orchestrator.update_player_state(request.scene_id, request.choice_index)
    
    # Generate agent response
    agent_response = agent.generate_response(
        scene_context=scene["description"],
        player_action=choice,
        historical_context=historical_context
    )
    
    # Generate voice for agent response
    audio_url = voice.text_to_speech(
        text=agent_response,
        emotion=agent.memory["mood"]
    )
    
    # Get next scene ID
    next_scene_id = scene["next_scene_map"][list("ABCD")[request.choice_index]]
    
    return {
        "agent_response": agent_response,
        "audio_url": audio_url,
        "next_scene_id": next_scene_id
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
