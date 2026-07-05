import React from 'react';

const Chart = ({ title, type = 'line', className = '' }) => {
  return (
    <div className={`p-6 bg-slate-900 border border-slate-800 rounded-2xl ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-semibold text-slate-350">{title || 'Data Visualization'}</h4>
        <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 bg-slate-800 px-2 py-0.5 rounded-full">{type}</span>
      </div>
      
      {/* Visual Chart Placeholder Design */}
      <div className="h-48 flex items-end justify-between gap-2 pt-4 relative">
        <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
          <div className="border-t border-slate-800/40 w-full h-0"></div>
          <div className="border-t border-slate-800/40 w-full h-0"></div>
          <div className="border-t border-slate-800/40 w-full h-0"></div>
        </div>
        
        {/* Sample bars to simulate rendering */}
        <div className="bg-brand-500/20 hover:bg-brand-500/30 border border-brand-500/40 rounded-t w-full transition-all duration-300" style={{ height: '40%' }}></div>
        <div className="bg-brand-500/20 hover:bg-brand-500/30 border border-brand-500/40 rounded-t w-full transition-all duration-300" style={{ height: '65%' }}></div>
        <div className="bg-brand-500/25 hover:bg-brand-500/35 border border-brand-500/50 rounded-t w-full transition-all duration-300" style={{ height: '50%' }}></div>
        <div className="bg-brand-500/30 hover:bg-brand-500/40 border border-brand-500/60 rounded-t w-full transition-all duration-300" style={{ height: '85%' }}></div>
        <div className="bg-brand-500/25 hover:bg-brand-500/35 border border-brand-500/50 rounded-t w-full transition-all duration-300" style={{ height: '70%' }}></div>
        <div className="bg-brand-500/40 hover:bg-brand-500/50 border border-brand-500/80 rounded-t w-full transition-all duration-300" style={{ height: '95%' }}></div>
      </div>
    </div>
  );
};

export default Chart;
