import React from 'react';

interface PlayerStatsProps {
  alignment: {
    law_chaos: number;
    good_evil: number;
  };
  experience: number;
  score: number;
  feedback: string;
}

const PlayerStats: React.FC<PlayerStatsProps> = ({ alignment, experience, score, feedback }) => {
  // Function to determine alignment label based on coordinates
  const getAlignmentLabel = () => {
    const { law_chaos, good_evil } = alignment;
    
    let lawChaosLabel = 'Neutral';
    if (law_chaos > 30) lawChaosLabel = 'Lawful';
    if (law_chaos < -30) lawChaosLabel = 'Chaotic';
    
    let goodEvilLabel = 'Neutral';
    if (good_evil > 30) goodEvilLabel = 'Good';
    if (good_evil < -30) goodEvilLabel = 'Evil';
    
    // Special case for true neutral
    if (lawChaosLabel === 'Neutral' && goodEvilLabel === 'Neutral') {
      return 'True Neutral';
    }
    
    return `${lawChaosLabel} ${goodEvilLabel}`;
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 mb-6 shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-center border-b border-gray-700 pb-2">Character Stats</h2>
      
      <div className="mb-4">
        <h3 className="font-semibold text-gray-400">Alignment</h3>
        <p className="text-lg">{getAlignmentLabel()}</p>
        <div className="grid grid-cols-2 gap-2 mt-2">
          <div className="text-sm">
            <span className="text-gray-400">Law/Chaos:</span> {alignment.law_chaos}
          </div>
          <div className="text-sm">
            <span className="text-gray-400">Good/Evil:</span> {alignment.good_evil}
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <h3 className="font-semibold text-gray-400">Experience</h3>
          <p className="text-lg">{experience}</p>
        </div>
        <div>
          <h3 className="font-semibold text-gray-400">Score</h3>
          <p className="text-lg">{score}</p>
        </div>
      </div>
      
      {feedback && (
        <div className="mt-4 border-t border-gray-700 pt-3">
          <h3 className="font-semibold text-gray-400 mb-2">Feedback</h3>
          <p className="text-sm italic">{feedback}</p>
        </div>
      )}
    </div>
  );
};

export default PlayerStats;
