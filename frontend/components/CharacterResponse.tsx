import React, { useEffect, useRef } from 'react';

interface CharacterResponseProps {
  response: string;
  audioUrl: string;
  characterName: string;
}

const CharacterResponse: React.FC<CharacterResponseProps> = ({ response, audioUrl, characterName }) => {
  const audioRef = useRef<HTMLAudioElement>(null);
  
  useEffect(() => {
    // Auto-play audio when available
    if (audioUrl && audioRef.current) {
      audioRef.current.play().catch(error => {
        console.error('Audio playback failed:', error);
      });
    }
  }, [audioUrl]);
  
  return (
    <div className="character-response mb-8 bg-gray-800 p-6 rounded-lg shadow-lg border-l-4 border-red-700">
      <h3 className="text-xl font-bold mb-2 text-red-500">{characterName} says:</h3>
      <p className="text-lg italic mb-4">"{response}"</p>
      
      {audioUrl && (
        <div className="audio-controls">
          <audio ref={audioRef} controls className="w-full">
            <source src={audioUrl} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
};

export default CharacterResponse;
