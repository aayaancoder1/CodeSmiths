import React, { createContext, useContext, useState, useCallback } from 'react';
import Toast from '../components/ui/Feedback/Toast';

const ToastContext = createContext(null);

let toastId = 0;

/**
 * ToastProvider wraps the app and provides global toast notifications.
 * Wrap around AppRoutes in main.jsx to enable.
 */
export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback(({ message, description, variant = 'info', duration = 4000 }) => {
    const id = ++toastId;
    setToasts((prev) => [...prev, { id, message, description, variant }]);

    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, duration);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      {/* Toast Stack — fixed bottom-right */}
      <div
        className="fixed bottom-5 right-5 z-[9999] flex flex-col gap-3 pointer-events-none"
        aria-live="polite"
        aria-atomic="false"
      >
        {toasts.map((toast) => (
          <Toast
            key={toast.id}
            message={toast.message}
            description={toast.description}
            variant={toast.variant}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

/**
 * useToast — returns { addToast } for triggering toast notifications.
 *
 * Example usage:
 * const { addToast } = useToast();
 * addToast({ message: 'Saved!', variant: 'success' });
 */
export const useToast = () => {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within a ToastProvider');
  return ctx;
};

export default ToastProvider;
