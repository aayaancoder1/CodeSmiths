import React from 'react';

const Card = ({
  title,
  subtitle,
  children,
  className = '',
  onClick,
  ...props
}) => {
  const isClickable = !!onClick;

  return (
    <div
      onClick={onClick}
      className={`bg-ui-surface border border-ui-border rounded-xl p-5 shadow-lg transition-all duration-150 ${
        isClickable 
          ? 'cursor-pointer hover:border-ui-borderHover hover:bg-ui-surfaceHover hover:shadow-xl active:scale-[0.99]' 
          : ''
      } ${className}`}
      {...props}
    >
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h4 className="text-sm font-semibold text-ui-text-primary">{title}</h4>}
          {subtitle && <p className="text-xs text-ui-text-tertiary mt-0.5">{subtitle}</p>}
        </div>
      )}
      <div className="text-sm text-ui-text-secondary">
        {children}
      </div>
    </div>
  );
};

export default Card;
