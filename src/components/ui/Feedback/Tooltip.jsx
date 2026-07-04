import React, { useState } from 'react';

const Tooltip = ({
  children,
  content,
  position = 'top', // 'top' | 'bottom' | 'left' | 'right'
  className = '',
  ...props
}) => {
  const [isVisible, setIsVisible] = useState(false);

  const positionStyles = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  const arrowStyles = {
    top: 'top-full left-1/2 -translate-x-1/2 border-t-ui-surface border-x-transparent border-b-transparent',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-b-ui-surface border-x-transparent border-t-transparent',
    left: 'left-full top-1/2 -translate-y-1/2 border-l-ui-surface border-y-transparent border-r-transparent',
    right: 'right-full top-1/2 -translate-y-1/2 border-r-ui-surface border-y-transparent border-l-transparent',
  };

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
      {...props}
    >
      {children}
      {isVisible && content && (
        <div
          role="tooltip"
          className={`absolute z-50 px-2 py-1 text-xs font-medium text-ui-text-primary bg-ui-surface border border-ui-border rounded shadow-xl whitespace-nowrap animate-fade-in pointer-events-none select-none ${positionStyles[position]} ${className}`}
        >
          {content}
          <div className={`absolute border-4 ${arrowStyles[position]}`} />
        </div>
      )}
    </div>
  );
};

export default Tooltip;
