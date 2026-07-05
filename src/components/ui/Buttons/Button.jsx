import React from 'react';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  className = '',
  onClick,
  type = 'button',
  ...props
}) => {
  // Styles based on the Design Token palette and hover/active states
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50 focus-visible:ring-offset-2 focus-visible:ring-offset-ui-bg select-none disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98]';

  const variants = {
    primary: 'bg-brand-500 hover:bg-brand-600 text-white shadow-md shadow-brand-500/10',
    secondary: 'bg-ui-surface hover:bg-ui-surfaceHover border border-ui-border text-ui-text-primary hover:border-ui-borderHover',
    outline: 'bg-transparent border border-ui-border text-ui-text-primary hover:bg-ui-surfaceHover hover:border-ui-borderHover',
    ghost: 'bg-transparent text-ui-text-secondary hover:text-ui-text-primary hover:bg-ui-surfaceHover',
    danger: 'bg-ui-danger-solid hover:bg-rose-600 text-white shadow-md shadow-ui-danger-solid/10',
    success: 'bg-ui-success-solid hover:bg-emerald-600 text-white shadow-md shadow-ui-success-solid/10',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-5 py-3 text-base',
  };

  const renderContent = () => {
    if (loading) {
      return (
        <span className="flex items-center gap-2">
          <svg className="animate-spin h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </span>
      );
    }
    return children;
  };

  return (
    <button
      type={type}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      aria-busy={loading}
      aria-disabled={disabled || loading}
      {...props}
    >
      {renderContent()}
    </button>
  );
};

export default Button;
