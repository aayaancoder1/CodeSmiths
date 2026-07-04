import React from 'react';

const Card = ({ title, value, change, changeType, icon, children, className = '' }) => {
  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm hover:border-slate-700/80 transition-all duration-200 ${className}`}>
      <div className="flex items-center justify-between">
        {title && <span className="text-sm font-medium text-slate-400">{title}</span>}
        {icon && <span className="text-xl select-none">{icon}</span>}
      </div>
      {(value || change) && (
        <div className="mt-2 flex items-baseline justify-between">
          {value && <span className="text-2xl font-bold tracking-tight text-white">{value}</span>}
          {change && (
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
              changeType === 'positive' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
            }`}>
              {change}
            </span>
          )}
        </div>
      )}
      {children && <div className="mt-4">{children}</div>}
    </div>
  );
};

export default Card;
