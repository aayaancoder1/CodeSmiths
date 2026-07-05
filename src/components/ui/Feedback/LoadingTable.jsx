import React from 'react';
import Skeleton from './Skeleton';

const LoadingTable = ({ rows = 4, className = '', ...props }) => {
  return (
    <div className={`border border-ui-border rounded-xl bg-ui-surface/30 p-4 space-y-4 ${className}`} {...props}>
      {/* Header Loading row */}
      <div className="flex justify-between items-center pb-3 border-b border-ui-border">
        <Skeleton variant="text" className="w-1/6 h-4" />
        <Skeleton variant="text" className="w-1/4 h-4" />
        <Skeleton variant="text" className="w-1/5 h-4" />
        <Skeleton variant="text" className="w-1/6 h-4" />
      </div>
      
      {/* Data loading rows */}
      {Array.from({ length: rows }).map((_, idx) => (
        <div key={idx} className="flex justify-between items-center py-2.5 border-b border-ui-divider/40 last:border-0">
          <Skeleton variant="text" className="w-1/12 h-3.5" />
          <Skeleton variant="text" className="w-1/3 h-3.5" />
          <Skeleton variant="text" className="w-1/6 h-3.5" />
          <Skeleton variant="text" className="w-1/12 h-3.5" />
        </div>
      ))}
    </div>
  );
};

export default LoadingTable;
