import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Layouts
import AuthLayout from '../layouts/AuthLayout/AuthLayout';
import MainLayout from '../layouts/MainLayout/MainLayout';

// Pages
import Login from '../pages/Login/Login';
import Dashboard from '../pages/Dashboard/Dashboard';
import Chat from '../pages/Chat/Chat';
import KnowledgeGraph from '../pages/KnowledgeGraph/KnowledgeGraph';
import HowItWorks from '../pages/HowItWorks/HowItWorks';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes with AuthLayout */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
        </Route>

        {/* Private/Protected Dashboard Routes with MainLayout */}
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/knowledge-graph" element={<KnowledgeGraph />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
        </Route>

        {/* Default Redirect from Root to Login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Catch-all Redirect to Login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;

