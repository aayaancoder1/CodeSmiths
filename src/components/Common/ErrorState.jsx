import React from 'react';

const ErrorState = ({ message = 'An unexpected error occurred.', onRetry, className = '' }) => {
  return (
    <div className={`flex flex-col items-center justify-center text-center p-8 rounded-2xl border border-red-900/30 bg-red-950/10 ${className}`}>
      <span className="text-4xl mb-4 select-none">⚠️</span>
      <h3 className="text-base font-semibold text-red-200">System Error</h3>
      <p className="mt-1 text-sm text-red-400/80 max-w-sm">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-6 px-4 py-2 bg-red-900/30 hover:bg-red-900/50 border border-red-800 text-red-200 text-sm font-medium rounded-lg transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
};

export default ErrorState;
