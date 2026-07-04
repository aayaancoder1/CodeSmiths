import React, { useState } from 'react';

const Avatar = ({
  src,
  alt = 'User avatar',
  name = '',
  size = 'md', // 'sm' | 'md' | 'lg' | 'xl'
  status = null, // 'online' | 'offline' | 'away' | 'busy' | null
  className = '',
  ...props
}) => {
  const [hasError, setHasError] = useState(false);

  const getInitials = (fullName) => {
    if (!fullName) return '';
    const parts = fullName.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  };

  const sizes = {
    sm: 'w-6 h-6 text-[10px]',
    md: 'w-8 h-8 text-xs',
    lg: 'w-10 h-10 text-sm',
    xl: 'w-12 h-12 text-base font-semibold',
  };

  const statusColors = {
    online: 'bg-emerald-500 ring-ui-bg',
    offline: 'bg-slate-500 ring-ui-bg',
    away: 'bg-amber-500 ring-ui-bg',
    busy: 'bg-rose-500 ring-ui-bg',
  };

  const statusSizes = {
    sm: 'w-1.5 h-1.5',
    md: 'w-2 h-2',
    lg: 'w-2.5 h-2.5',
    xl: 'w-3 h-3',
  };

  const renderFallback = () => {
    if (name) {
      return (
        <div className="flex items-center justify-center w-full h-full rounded-full bg-brand-500/10 text-brand-400 font-medium uppercase border border-brand-500/20">
          {getInitials(name)}
        </div>
      );
    }
    return (
      <div className="flex items-center justify-center w-full h-full rounded-full bg-ui-surface text-ui-text-tertiary border border-ui-border">
        <svg className="w-[60%] h-[60%]" fill="currentColor" viewBox="0 0 24 24">
          <path fillRule="evenodd" d="M12 2a5 5 0 00-5 5v3a5 5 0 0010 0V7a5 5 0 00-5-5zM5 20a7 7 0 0114 0v1H5v-1z" clipRule="evenodd" />
        </svg>
      </div>
    );
  };

  return (
    <div className={`relative inline-block select-none ${className}`} {...props}>
      <div className={`${sizes[size]} rounded-full overflow-hidden flex items-center justify-center`}>
        {src && !hasError ? (
          <img
            src={src}
            alt={alt}
            onError={() => setHasError(true)}
            className="w-full h-full object-cover"
          />
        ) : (
          renderFallback()
        )}
      </div>

      {status && statusColors[status] && (
        <span
          className={`absolute bottom-0 right-0 rounded-full ring-2 ${statusColors[status]} ${statusSizes[size]}`}
          aria-label={`Status: ${status}`}
        />
      )}
    </div>
  );
};

export default Avatar;
