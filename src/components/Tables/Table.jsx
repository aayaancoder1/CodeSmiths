import React from 'react';

const Table = ({ headers = [], children, className = '' }) => {
  return (
    <div className={`overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/50 ${className}`}>
      <table className="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-300">
        <thead className="bg-slate-900 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          <tr>
            {headers.map((header, idx) => (
              <th key={idx} className="px-6 py-4 font-semibold">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 bg-slate-900/20">
          {children}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
