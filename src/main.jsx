import React from 'react'
import ReactDOM from 'react-dom/client'
import AppRoutes from './routes/AppRoutes.jsx'
import './index.css'
import { ToastProvider } from './context/ToastContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ToastProvider>
      <AppRoutes />
    </ToastProvider>
  </React.StrictMode>,
)
