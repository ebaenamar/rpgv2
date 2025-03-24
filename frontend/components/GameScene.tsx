import React from 'react';

interface GameSceneProps {
  description: string;
  imageUrl: string;
}

const GameScene: React.FC<GameSceneProps> = ({ description, imageUrl }) => {
  return (
    <div className="game-scene mb-8">
      <div className="scene-image mb-4 rounded-lg overflow-hidden shadow-lg">
        {imageUrl ? (
          <img 
            src={imageUrl} 
            alt="Scene" 
            className="w-full h-64 md:h-96 object-cover"
          />
        ) : (
          <div className="w-full h-64 md:h-96 bg-gray-700 flex items-center justify-center">
            <p>Loading scene image...</p>
          </div>
        )}
      </div>
      
      <div className="scene-description bg-gray-800 p-6 rounded-lg shadow-inner">
        <p className="text-lg">{description}</p>
      </div>
    </div>
  );
};

export default GameScene;
