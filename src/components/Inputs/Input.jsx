import React from 'react';

const Input = ({ label, error, className = '', ...props }) => {
  return (
    <div className={`space-y-1.5 ${className}`}>
      {label && <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</label>}
      <input
        className={`w-full bg-slate-950 border text-slate-200 rounded-xl px-4 py-2.5 text-sm transition-colors duration-200 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 placeholder-slate-650 ${
          error ? 'border-rose-500/50 focus:border-rose-500' : 'border-slate-800 hover:border-slate-700'
        }`}
        {...props}
      />
      {error && <p className="text-xs text-rose-450">{error}</p>}
    </div>
  );
};

export default Input;
