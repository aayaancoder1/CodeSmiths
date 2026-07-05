import React from 'react';
import Spinner from './Spinner';

const Loading = ({
  loading = true,
  children,
  overlay = false,
  message = 'Loading...',
  size = 'md',
  className = '',
  ...props
}) => {
  if (!loading) return children || null;

  if (overlay) {
    return (
      <div className={`relative ${className}`} {...props}>
        {children}
        <div className="absolute inset-0 bg-ui-bg/75 backdrop-blur-[2px] flex flex-col gap-3 justify-center items-center z-40 transition-all duration-200">
          <Spinner size={size} />
          {message && <span className="text-sm font-medium text-ui-text-secondary">{message}</span>}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col gap-3 justify-center items-center py-12 ${className}`} {...props}>
      <Spinner size={size} />
      {message && <span className="text-xs font-medium text-ui-text-tertiary">{message}</span>}
    </div>
  );
};

export default Loading;
