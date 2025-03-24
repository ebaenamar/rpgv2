import { useState, useEffect } from 'react';
import Head from 'next/head';
import axios from 'axios';
import GameScene from '../components/GameScene';
import CharacterResponse from '../components/CharacterResponse';
import PlayerChoices from '../components/PlayerChoices';
import LoadingIndicator from '../components/LoadingIndicator';

// Define API URL based on environment
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [scene, setScene] = useState(null);
  const [choices, setChoices] = useState([]);
  const [agentResponse, setAgentResponse] = useState('');
  const [sceneImage, setSceneImage] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [gameStarted, setGameStarted] = useState(false);
  const [nextSceneId, setNextSceneId] = useState('');
  const [showContinue, setShowContinue] = useState(false);
  
  // Start the game
  const startGame = async () => {
    setGameStarted(true);
    await fetchScene('intro');
  };
  
  // Fetch scene data from API
  const fetchScene = async (sceneId) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/scene/${sceneId}`);
      setScene(response.data.scene);
      setChoices(response.data.choices);
      setSceneImage(response.data.image_url);
      setAgentResponse(''); // Clear previous agent response
      setAudioUrl(''); // Clear previous audio
    } catch (error) {
      console.error('Error fetching scene:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Handle player choice
  const makeChoice = async (choiceIndex) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/action`, {
        scene_id: scene.scene_id,
        choice_index: choiceIndex
      });
      
      setAgentResponse(response.data.agent_response);
      setAudioUrl(response.data.audio_url);
      
      // Don't automatically move to the next scene
      // Instead, show a continue button after the response
      setLoading(false);
      
      // Store the next scene ID for when the player continues
      setNextSceneId(response.data.next_scene_id);
    } catch (error) {
      console.error('Error making choice:', error);
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Head>
        <title>RPG Maestro - Medieval Adventure</title>
        <meta name="description" content="An AI-powered medieval RPG game" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">RPG Maestro</h1>
        
        {!gameStarted ? (
          <div className="text-center">
            <h2 className="text-2xl mb-4">Medieval Adventure</h2>
            <p className="mb-6">Embark on a journey through 13th century England with your companion, Ser Elyen. Make choices that affect your alignment and relationship with your companion.</p>
            <button 
              onClick={startGame}
              className="bg-red-700 hover:bg-red-800 text-white font-bold py-3 px-6 rounded-lg transition duration-300"
            >
              Begin Your Adventure
            </button>
          </div>
        ) : loading ? (
          <LoadingIndicator />
        ) : (
          <div className="game-container">
            <GameScene 
              description={scene?.description} 
              imageUrl={sceneImage} 
            />
            
            {agentResponse && (
              <div className="mb-6">
                <CharacterResponse 
                  response={agentResponse} 
                  audioUrl={audioUrl} 
                  characterName="Ser Elyen"
                />
                
                {/* Add continue button after character response */}
                <div className="mt-6 text-center">
                  <button 
                    onClick={() => {
                      setAgentResponse('');
                      setAudioUrl('');
                      fetchScene(nextSceneId);
                    }}
                    className="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-4 rounded-lg transition duration-300"
                  >
                    Continue Your Journey
                  </button>
                </div>
              </div>
            )}
            
            {!agentResponse && (
              <PlayerChoices 
                choices={choices} 
                onChoiceSelected={makeChoice} 
              />
            )}
          </div>
        )}
      </main>
      
      <footer className="text-center py-4 text-gray-400 text-sm">
        Powered by AI21 Maestro, Replicate, and Sesame Maya
      </footer>
    </div>
  );
}
