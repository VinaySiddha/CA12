import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';

// Components
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Matches from './pages/Matches';
import StudyGroups from './pages/StudyGroups';
import Resources from './pages/Resources';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-white relative">
          {/* Main Content */}
          <div className="relative z-10">
            <Navbar />
              
              <main className="container mx-auto px-4 py-8">
                <Routes>
                  {/* Public Routes */}
                  <Route path="/" element={<LandingPage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  
                  {/* Protected Routes */}
                  <Route path="/dashboard" element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/profile" element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/matches" element={
                    <ProtectedRoute>
                      <Matches />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/study-groups" element={
                    <ProtectedRoute>
                      <StudyGroups />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/resources" element={
                    <ProtectedRoute>
                      <Resources />
                    </ProtectedRoute>
                  } />
                  
                  {/* 404 Page */}
                  <Route path="*" element={<div className="text-black text-center py-20">Page Not Found</div>} />
                </Routes>
              </main>
            </div>
            
            {/* Toast Notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'white',
                  color: 'black',
                  border: '1px solid #e5e7eb',
                  borderRadius: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                },
                success: {
                  iconTheme: {
                    primary: '#22c55e',
                    secondary: 'white',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: 'white',
                  },
                },
              }}
            />
          </div>
        </Router>
      </AuthProvider>
  );
}

export default App;