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
      
      // Move to next scene after delay
      setTimeout(() => {
        fetchScene(response.data.next_scene_id);
      }, 6000); // Give time to hear/read the response
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
              <CharacterResponse 
                response={agentResponse} 
                audioUrl={audioUrl} 
                characterName="Ser Elyen"
              />
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
