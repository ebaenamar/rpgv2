import { useState, useEffect } from 'react';
import Head from 'next/head';
import axios from 'axios';
import GameScene from '../components/GameScene';
import CharacterResponse from '../components/CharacterResponse';
import PlayerChoices from '../components/PlayerChoices';
import LoadingIndicator from '../components/LoadingIndicator';
import HistoricalFacts from '../components/HistoricalFacts';
import PlayerStats from '../components/PlayerStats';

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
  const [historicalFacts, setHistoricalFacts] = useState([]);
  const [playerState, setPlayerState] = useState({
    alignment: { law_chaos: 0, good_evil: 0 },
    experience: 0,
    score: 0,
    skills: {}
  });
  const [feedback, setFeedback] = useState('');
  
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
      setHistoricalFacts(response.data.historical_context || []);
      setAgentResponse(''); // Clear previous agent response
      setAudioUrl(''); // Clear previous audio
      
      // Update player state if available
      if (response.data.player_state) {
        setPlayerState(response.data.player_state);
      }
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
      setHistoricalFacts(response.data.historical_context || []);
      
      // Don't automatically move to the next scene
      // Instead, show a continue button after the response
      setLoading(false);
      
      // Store the next scene ID for when the player continues
      setNextSceneId(response.data.next_scene_id);
      
      // Update player state if available
      if (response.data.player_state) {
        setPlayerState(response.data.player_state);
      }
      
      // Set feedback if available
      if (response.data.scoring && response.data.scoring.feedback) {
        setFeedback(response.data.scoring.feedback);
      } else {
        setFeedback('');
      }
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
          <div className="grid grid-cols-12 gap-4">
            {/* Left Column - Player Stats and Historical Facts */}
            <div className="col-span-3">
              <PlayerStats 
                alignment={playerState.alignment}
                experience={playerState.experience}
                score={playerState.score}
                feedback={feedback}
              />
              
              <HistoricalFacts facts={historicalFacts} />
            </div>
            
            {/* Center Column - Game Scene and Character Response */}
            <div className="col-span-6">
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
                </div>
              )}
            </div>
            
            {/* Right Column - Player Choices or Continue Button */}
            <div className="col-span-3">
              {agentResponse ? (
                <div className="mt-4">
                  <h3 className="text-xl font-bold mb-4">Ready to continue?</h3>
                  <button
                    onClick={() => {
                      setAgentResponse('');
                      setAudioUrl('');
                      fetchScene(nextSceneId);
                    }}
                    className="w-full bg-green-700 hover:bg-green-800 text-white font-bold py-4 px-6 rounded-lg transition duration-300"
                  >
                    Continue Journey
                  </button>
                </div>
              ) : (
                <PlayerChoices 
                  choices={choices} 
                  onChoiceSelected={makeChoice} 
                />
              )}
            </div>
          </div>
        )}
      </main>
      
      <footer className="text-center py-4 text-gray-400 text-sm">
        Powered by AI21 Maestro, Replicate, and Sesame Maya
      </footer>
    </div>
  );
}
