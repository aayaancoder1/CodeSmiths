import React from 'react';

const SearchInput = ({
  value = '',
  onChange,
  onClear,
  placeholder = 'Search...',
  className = '',
  disabled = false,
  ...props
}) => {
  const handleChange = (e) => {
    if (onChange) onChange(e.target.value);
  };

  const handleClear = () => {
    if (onClear) onClear();
  };

  return (
    <div className={`relative flex items-center w-full ${className}`}>
      {/* Search Icon */}
      <span className="absolute left-3.5 text-ui-text-tertiary select-none pointer-events-none">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </span>

      <input
        type="text"
        value={value}
        onChange={handleChange}
        disabled={disabled}
        placeholder={placeholder}
        className="w-full bg-ui-bg border border-ui-border text-ui-text-primary rounded-lg text-sm transition-colors duration-150 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 placeholder-ui-text-tertiary disabled:opacity-50 disabled:bg-ui-surface pl-10 pr-10 py-2.5 hover:border-ui-borderHover"
        {...props}
      />

      {/* Clear Button */}
      {value && !disabled && (
        <button
          type="button"
          onClick={handleClear}
          className="absolute right-3.5 p-1 rounded-md text-ui-text-tertiary hover:text-ui-text-primary hover:bg-ui-surface transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
          aria-label="Clear search"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default SearchInput;
