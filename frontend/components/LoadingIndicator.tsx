import React from 'react';

const LoadingIndicator: React.FC = () => {
  return (
    <div className="loading-indicator flex flex-col items-center justify-center py-12">
      <div className="spinner mb-4">
        <div className="w-16 h-16 border-4 border-gray-600 border-t-red-600 rounded-full animate-spin"></div>
      </div>
      <p className="text-lg">Loading your adventure...</p>
    </div>
  );
};

export default LoadingIndicator;
