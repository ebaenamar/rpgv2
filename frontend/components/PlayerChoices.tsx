import React from 'react';

interface PlayerChoicesProps {
  choices: string[];
  onChoiceSelected: (index: number) => void;
}

const PlayerChoices: React.FC<PlayerChoicesProps> = ({ choices, onChoiceSelected }) => {
  return (
    <div className="player-choices">
      <h3 className="text-xl font-bold mb-4">What will you do?</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {choices.map((choice, index) => (
          <button
            key={index}
            onClick={() => onChoiceSelected(index)}
            className="choice-button bg-gray-800 hover:bg-gray-700 text-white font-medium py-4 px-6 rounded-lg border border-gray-600 transition duration-300 text-left"
          >
            {choice}
          </button>
        ))}
      </div>
    </div>
  );
};

export default PlayerChoices;
