import React from 'react';
import Skeleton from './Skeleton';

const LoadingCard = ({ className = '', ...props }) => {
  return (
    <div className={`p-5 bg-ui-surface border border-ui-border rounded-xl space-y-4 shadow-lg ${className}`} {...props}>
      <div className="flex justify-between items-center">
        <Skeleton variant="text" className="w-1/3 h-3" />
        <Skeleton variant="circle" className="w-6 h-6" />
      </div>
      <Skeleton variant="text" className="w-1/2 h-8" />
      <Skeleton variant="text" className="w-1/4 h-3.5" />
    </div>
  );
};

export default LoadingCard;
