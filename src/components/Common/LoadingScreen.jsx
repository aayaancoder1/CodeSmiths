import React from 'react';

const LoadingScreen = ({ message = 'Loading workspace...', className = '' }) => {
  return (
    <div className={`min-h-[400px] w-full flex flex-col items-center justify-center space-y-4 ${className}`}>
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-slate-800"></div>
        <div className="absolute inset-0 rounded-full border-4 border-brand-500 border-t-transparent animate-spin"></div>
      </div>
      <p className="text-sm font-medium text-slate-400 animate-pulse">{message}</p>
    </div>
  );
};

export default LoadingScreen;
