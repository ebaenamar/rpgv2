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
          <div className="flex items-center">
            <p className="text-lg mr-2">{experience}</p>
            <div className="w-full bg-gray-700 rounded-full h-2.5">
              <div 
                className="bg-blue-500 h-2.5 rounded-full" 
                style={{ width: `${Math.min(100, (experience / 100) * 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
        <div>
          <h3 className="font-semibold text-gray-400">Score</h3>
          <div className="flex items-center">
            <p className="text-lg mr-2">{Math.round(score)}</p>
            <div className="w-full bg-gray-700 rounded-full h-2.5">
              <div 
                className="bg-green-500 h-2.5 rounded-full" 
                style={{ width: `${Math.min(100, (score / 100) * 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
      
      {feedback && (
        <div className="mt-4 border-t border-gray-700 pt-3">
          <h3 className="font-semibold text-gray-400 mb-2">Feedback</h3>
          <div className="p-3 bg-gray-700 rounded-lg">
            <p className="text-sm italic">{feedback}</p>
          </div>
        </div>
      )}
      
      {/* Alignment Chart Visualization */}
      <div className="mt-4 border-t border-gray-700 pt-3">
        <h3 className="font-semibold text-gray-400 mb-2">Alignment Chart</h3>
        <div className="relative w-full h-32 bg-gray-700 rounded-lg overflow-hidden">
          {/* Vertical axis line */}
          <div className="absolute top-0 bottom-0 left-1/2 w-0.5 bg-gray-600"></div>
          {/* Horizontal axis line */}
          <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-gray-600"></div>
          
          {/* Labels */}
          <div className="absolute top-1 left-1 text-xs text-gray-400">Lawful Good</div>
          <div className="absolute top-1 right-1 text-xs text-gray-400">Lawful Evil</div>
          <div className="absolute bottom-1 left-1 text-xs text-gray-400">Chaotic Good</div>
          <div className="absolute bottom-1 right-1 text-xs text-gray-400">Chaotic Evil</div>
          
          {/* Character position marker */}
          <div 
            className="absolute w-3 h-3 bg-yellow-500 rounded-full transform -translate-x-1/2 -translate-y-1/2"
            style={{ 
              left: `${50 + (alignment.law_chaos / 100) * 50}%`, 
              top: `${50 + (alignment.good_evil / 100) * 50}%` 
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default PlayerStats;
