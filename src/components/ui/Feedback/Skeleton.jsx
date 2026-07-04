import React from 'react';

const Skeleton = ({
  variant = 'text', // 'text' | 'rect' | 'circle'
  className = '',
  ...props
}) => {
  const styles = {
    text: 'h-4 w-3/4 rounded',
    rect: 'h-24 w-full rounded-lg',
    circle: 'h-10 w-10 rounded-full',
  };

  return (
    <div 
      className={`bg-slate-800 animate-pulse ${styles[variant]} ${className}`} 
      {...props} 
    />
  );
};

export default Skeleton;
