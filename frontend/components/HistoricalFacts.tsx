import React from 'react';

interface HistoricalFactsProps {
  facts: Array<{
    title?: string;
    content?: string;
    text?: string;
    source?: string;
  }>;
}

const HistoricalFacts: React.FC<HistoricalFactsProps> = ({ facts }) => {
  if (!facts || facts.length === 0) {
    return null;
  }

  return (
    <div className="bg-gray-800 rounded-lg p-4 shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-center border-b border-gray-700 pb-2">Historical Context</h2>
      
      <div className="space-y-4">
        {facts.map((fact, index) => (
          <div key={index} className="mb-3">
            <h3 className="font-semibold text-yellow-500">{fact.title || fact.source}</h3>
            <p className="text-sm text-gray-300">{fact.content || fact.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoricalFacts;
