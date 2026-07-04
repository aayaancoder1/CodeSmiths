import React from 'react';
import Card from './Card';

const AdminCard = ({
  name,
  role,
  avatarUrl,
  initials = 'US',
  status = 'active', // 'active' | 'suspended'
  actions,
  className = '',
  ...props
}) => {
  return (
    <Card className={`hover:border-ui-borderHover ${className}`} {...props}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Avatar Profile Initials */}
          <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-ui-text-primary select-none">
            {initials.toUpperCase()}
          </div>

          <div>
            <h5 className="text-sm font-semibold text-white">{name}</h5>
            <p className="text-xs text-ui-text-tertiary mt-0.5">{role}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
            status === 'active' ? 'bg-ui-success-bg/15 text-ui-success-text' : 'bg-ui-danger-bg/15 text-ui-danger-text'
          }`}>
            {status}
          </span>
          {actions && <div className="flex items-center gap-1">{actions}</div>}
        </div>
      </div>
    </Card>
  );
};

export default AdminCard;
