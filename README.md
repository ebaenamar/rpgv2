# RPG Maestro - AI-Powered Medieval Adventure Game

An agentic RPG game system powered by AI21 Labs' Maestro framework, featuring dynamic storytelling, historical context via RAG, moral decision-making, and an interactive LLM-driven NPC. The game includes scene visualization with Replicate and voice synthesis with Sesame Maya.

## Project Structure

```
rpg_maestro/
├── api/                # FastAPI backend
│   ├── game/           # Game logic components
│   │   ├── agent.py    # MaestroCharacterAgent implementation
│   │   ├── orchestrator.py # Game orchestration logic
│   │   ├── rag.py      # Retrieval-Augmented Generation system
│   │   ├── visualizer.py # Scene image generation
│   │   └── voice.py    # Voice synthesis with Sesame Maya
│   └── main.py         # FastAPI application
├── frontend/           # Next.js frontend
│   ├── components/     # React components
│   ├── pages/          # Next.js pages
│   └── styles/         # CSS styles
├── requirements.txt    # Python dependencies
└── render.yaml         # Render deployment configuration
```

## Features

- **AI21 Maestro Integration**: Structured and reliable character responses with validation
- **Historical Context**: RAG system provides accurate medieval facts
- **Dynamic Storytelling**: Player choices affect character relationships and story progression
- **Scene Visualization**: Generated images for each scene using Replicate
- **Voice Synthesis**: Character dialogue voiced by Sesame Maya
- **Moral Decision System**: Track player alignment on Law-Chaos and Good-Evil axes

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 14+
- API keys for:
  - AI21 Labs (for Maestro)
  - Replicate (for image generation)
  - Sesame AI (for voice synthesis)

### Backend Setup

1. Navigate to the project directory:
   ```
   cd rpg_maestro
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   AI21_API_KEY=your_ai21_api_key
   REPLICATE_API_TOKEN=your_replicate_api_token
   SESAME_API_KEY=your_sesame_api_key
   ```

4. Run the backend locally:
   ```
   uvicorn api.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd rpg_maestro/frontend
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Create a `.env.local` file with the backend URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Run the frontend development server:
   ```
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:3000`

## Deployment

### Backend Deployment (Render)

1. Push your code to GitHub
2. Connect your GitHub repository to Render
3. Create a new Web Service, selecting the repository
4. Render will automatically detect the `render.yaml` configuration
5. Add your environment variables (API keys) in the Render dashboard
6. Deploy the service

### Frontend Deployment

1. Build the frontend for production:
   ```
   cd frontend
   npm run build
   ```

2. Deploy the frontend to your preferred hosting service (Vercel, Netlify, etc.)
3. Set the environment variable `NEXT_PUBLIC_API_URL` to your Render backend URL

## License

MIT
