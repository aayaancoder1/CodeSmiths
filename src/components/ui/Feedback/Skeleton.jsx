import React from 'react';

const Skeleton = ({
  variant = 'text', // 'text' | 'rect' | 'circle' | 'card'
  className = '',
  lines = 1, // number of lines for 'text' variant
  ...props
}) => {
  const baseClasses = 'bg-ui-surface/80 animate-pulse rounded';

  if (variant === 'text' && lines > 1) {
    return (
      <div className={`space-y-2 ${className}`} {...props}>
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className={`${baseClasses} h-3.5 ${i === lines - 1 ? 'w-3/5' : 'w-full'}`}
          />
        ))}
      </div>
    );
  }

  const styles = {
    text: `h-4 w-3/4 ${baseClasses}`,
    rect: `h-24 w-full rounded-lg ${baseClasses}`,
    circle: `h-10 w-10 rounded-full ${baseClasses}`,
    card: `h-32 w-full rounded-xl ${baseClasses}`,
  };

  return (
    <div
      className={`${styles[variant] || styles.text} ${className}`}
      aria-hidden="true"
      {...props}
    />
  );
};

export default Skeleton;
