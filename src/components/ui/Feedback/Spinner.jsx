import React from 'react';

const Spinner = ({
  size = 'md', // 'sm' | 'md' | 'lg'
  className = '',
  ...props
}) => {
  const sizes = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div className={`relative ${sizes[size]} ${className}`} role="status" {...props}>
      <span className="sr-only">Loading...</span>
      <div className="absolute inset-0 rounded-full border-ui-border"></div>
      <div className="absolute inset-0 rounded-full border-brand-500 border-t-transparent animate-spin"></div>
    </div>
  );
};

export default Spinner;
