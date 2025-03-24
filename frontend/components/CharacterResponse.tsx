import React, { useState, useRef } from 'react';

interface CharacterResponseProps {
  response: string;
  audioUrl: string;
  characterName: string;
}

const CharacterResponse: React.FC<CharacterResponseProps> = ({ response, audioUrl, characterName }) => {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // Character avatar image - using a fixed medieval knight image for now
  const characterImage = 'https://placehold.co/100x100/7D3C98/FFFFFF?text=Knight';
  
  const handlePlayAudio = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play().catch(error => {
          console.error('Audio playback failed:', error);
        });
      }
      setIsPlaying(!isPlaying);
    }
  };
  
  return (
    <div className="character-response mb-8">
      {/* Comic-style vignette */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg border-2 border-red-700 relative overflow-hidden">
        {/* Speech bubble with tail */}
        <div className="relative bg-white text-black p-4 rounded-lg mb-4 mx-4">
          <div className="absolute bottom-0 left-6 transform translate-y-1/2 rotate-45 w-4 h-4 bg-white"></div>
          <p className="text-lg italic z-10 relative">"{response}"</p>
        </div>
        
        {/* Character image and name */}
        <div className="flex items-center">
          <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-red-500 flex-shrink-0">
            <img src={characterImage} alt={characterName} className="w-full h-full object-cover" />
          </div>
          <div className="ml-4">
            <h3 className="text-xl font-bold text-red-500">{characterName}</h3>
            
            {/* Audio controls */}
            {audioUrl && (
              <div className="audio-controls flex items-center mt-2">
                <button 
                  onClick={handlePlayAudio}
                  className="bg-red-600 hover:bg-red-700 text-white rounded-full p-2 mr-2 focus:outline-none"
                >
                  {isPlaying ? (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
                <span className="text-sm text-gray-400">Listen to voice</span>
                <audio ref={audioRef} className="hidden">
                  <source src={audioUrl} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CharacterResponse;
