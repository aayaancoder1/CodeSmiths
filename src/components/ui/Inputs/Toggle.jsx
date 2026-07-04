import React from 'react';

const Toggle = ({
  label,
  checked,
  onChange,
  disabled = false,
  className = '',
  id,
  ...props
}) => {
  const toggleId = id || `toggle-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={`flex items-center gap-3 select-none ${className}`}>
      <button
        id={toggleId}
        type="button"
        role="switch"
        aria-checked={checked}
        disabled={disabled}
        onClick={() => onChange && onChange(!checked)}
        className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:ring-offset-2 focus:ring-offset-ui-bg disabled:opacity-50 ${
          checked ? 'bg-brand-500' : 'bg-ui-surface border-ui-border'
        }`}
        {...props}
      >
        <span
          className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
            checked ? 'translate-x-5' : 'translate-x-0'
          }`}
        />
      </button>
      {label && (
        <label
          htmlFor={toggleId}
          className="text-sm font-medium text-ui-text-secondary cursor-pointer"
        >
          {label}
        </label>
      )}
    </div>
  );
};

export default Toggle;
