import React from 'react';

const Radio = ({
  label,
  name,
  value,
  checked,
  onChange,
  disabled = false,
  className = '',
  id,
  ...props
}) => {
  const radioId = id || `radio-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={`flex items-center gap-2.5 select-none ${className}`}>
      <input
        id={radioId}
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onChange={(e) => onChange && onChange(e.target.value)}
        disabled={disabled}
        className="w-4 h-4 bg-ui-bg border border-ui-border rounded-full text-brand-500 transition-all duration-150 focus:ring-2 focus:ring-brand-500/20 disabled:opacity-50 checked:bg-brand-500"
        {...props}
      />
      {label && (
        <label
          htmlFor={radioId}
          className="text-sm font-medium text-ui-text-secondary cursor-pointer"
        >
          {label}
        </label>
      )}
    </div>
  );
};

export default Radio;
