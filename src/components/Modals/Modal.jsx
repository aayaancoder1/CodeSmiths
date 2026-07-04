import React from 'react';

const Modal = ({ isOpen, onClose, title, children, className = '' }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Overlay Backdrop */}
      <div 
        className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity" 
        onClick={onClose}
      />
      
      {/* Modal Dialog */}
      <div className={`relative w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl z-10 transform scale-100 transition-all ${className}`}>
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <h3 className="text-lg font-bold text-white">{title || 'Notification'}</h3>
          <button 
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 transition-colors p-1.5 rounded-lg hover:bg-slate-800"
          >
            ✕
          </button>
        </div>
        <div className="text-sm text-slate-350 space-y-4">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
