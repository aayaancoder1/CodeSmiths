import React from 'react';

const Tabs = ({
  tabs = [], // array of { id, label, icon, disabled }
  activeTab,
  onChange,
  className = '',
  ...props
}) => {
  return (
    <div className={`border-b border-ui-divider ${className}`} {...props}>
      <nav className="flex gap-6 -mb-px overflow-x-auto scrollbar-none" aria-label="Tabs">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const isDisabled = tab.disabled;

          return (
            <button
              key={tab.id}
              onClick={() => !isDisabled && onChange && onChange(tab.id)}
              disabled={isDisabled}
              className={`flex items-center gap-2 py-4 px-1 text-xs font-semibold uppercase tracking-wider border-b-2 transition-all duration-150 whitespace-nowrap focus:outline-none ${
                isActive
                  ? 'border-brand-500 text-brand-400 font-bold'
                  : 'border-transparent text-ui-text-secondary hover:text-ui-text-primary hover:border-ui-borderHover'
              } ${isDisabled ? 'opacity-40 cursor-not-allowed pointer-events-none' : 'cursor-pointer'}`}
              aria-current={isActive ? 'page' : undefined}
            >
              {tab.icon && <span className="flex-shrink-0">{tab.icon}</span>}
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
};

export default Tabs;
