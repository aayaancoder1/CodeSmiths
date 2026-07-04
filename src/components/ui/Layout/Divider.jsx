import React from 'react';

const Divider = ({
  orientation = 'horizontal', // 'horizontal' | 'vertical'
  label,
  className = '',
  ...props
}) => {
  if (orientation === 'vertical') {
    return (
      <div 
        className={`w-px self-stretch bg-ui-divider ${className}`} 
        role="separator" 
        aria-orientation="vertical"
        {...props} 
      />
    );
  }

  if (label) {
    return (
      <div className={`flex items-center w-full my-4 ${className}`} role="separator" aria-orientation="horizontal" {...props}>
        <div className="flex-1 border-t border-ui-divider"></div>
        <span className="px-3 text-[10px] uppercase font-bold tracking-widest text-ui-text-tertiary select-none">
          {label}
        </span>
        <div className="flex-1 border-t border-ui-divider"></div>
      </div>
    );
  }

  return (
    <div 
      className={`w-full border-t border-ui-divider my-4 ${className}`} 
      role="separator" 
      aria-orientation="horizontal"
      {...props} 
    />
  );
};

export default Divider;
