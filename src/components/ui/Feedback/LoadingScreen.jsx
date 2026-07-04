import React from 'react';
import Spinner from './Spinner';

const LoadingScreen = ({ message = 'Loading source nodes...', className = '', ...props }) => {
  return (
    <div className={`min-h-[400px] w-full flex flex-col items-center justify-center space-y-4 ${className}`} {...props}>
      <Spinner size="lg" />
      <p className="text-sm font-semibold text-ui-text-secondary animate-pulse">{message}</p>
    </div>
  );
};

export default LoadingScreen;
