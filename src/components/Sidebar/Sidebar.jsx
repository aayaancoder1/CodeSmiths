import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ className = '' }) => {
  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: '📊' },
    { name: 'Chat UI', path: '/chat', icon: '💬' },
    { name: 'Search UI', path: '/search', icon: '🔍' },
    { name: 'Knowledge Graph', path: '/knowledge-graph', icon: '🕸️' },
    { name: 'Analytics', path: '/analytics', icon: '📈' },
    { name: 'Admin Dashboard', path: '/admin', icon: '🛡️' },
  ];

  return (
    <aside className={`w-64 bg-slate-900 border-r border-slate-800 flex flex-col shrink-0 ${className}`}>
      {/* Brand Logo Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800">
        <span className="text-lg font-bold text-white tracking-wider flex items-center gap-2">
          <span>🛠️</span> CodeSmiths
        </span>
      </div>

      {/* Navigation Links */}
      <nav className="flex-grow p-4 space-y-1">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/20'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`
            }
          >
            <span className="text-lg mr-3 select-none">{item.icon}</span>
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500 text-center">
        v1.0.0 · Thanmayee (Frontend)
      </div>
    </aside>
  );
};

export default Sidebar;
