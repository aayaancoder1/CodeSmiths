import React from 'react';

const IconButton = ({
  icon,
  variant = 'secondary',
  size = 'md',
  disabled = false,
  className = '',
  onClick,
  'aria-label': ariaLabel,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center rounded-lg transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50 focus-visible:ring-offset-2 focus-visible:ring-offset-ui-bg disabled:opacity-50 disabled:pointer-events-none active:scale-[0.95]';

  const variants = {
    primary: 'bg-brand-500 hover:bg-brand-600 text-white',
    secondary: 'bg-ui-surface hover:bg-ui-surfaceHover border border-ui-border text-ui-text-secondary hover:text-ui-text-primary hover:border-ui-borderHover',
    outline: 'bg-transparent border border-ui-border text-ui-text-secondary hover:text-ui-text-primary hover:bg-ui-surfaceHover hover:border-ui-borderHover',
    ghost: 'bg-transparent text-ui-text-secondary hover:text-ui-text-primary hover:bg-ui-surfaceHover',
  };

  const sizes = {
    sm: 'p-1.5 text-xs',
    md: 'p-2 text-sm',
    lg: 'p-3 text-base',
  };

  return (
    <button
      type="button"
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled}
      onClick={onClick}
      aria-label={ariaLabel}
      {...props}
    >
      <span className="flex items-center justify-center leading-none select-none">{icon}</span>
    </button>
  );
};

export default IconButton;
