import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';

// Components
import NewNavbar from './components/layout/NewNavbar';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import LandingPage from './pages/LandingPage-new';
import LoginPage from './pages/LoginPage-new';
import RegisterPage from './pages/RegisterPage-new';
import Dashboard from './pages/Dashboard-new';
import Profile from './pages/Profile-new';
import Matches from './pages/Matches-new';
import StudyGroups from './pages/StudyGroups-new';
import Resources from './pages/Resources-new';

// Role-specific Pages
import StudentsPage from './pages/StudentsPage';
import CreateGroupsPage from './pages/CreateGroupsPage';
import ViewFeedbackPage from './pages/ViewFeedbackPage';
import AdminPanel from './pages/AdminPanel';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="bg-background-light dark:bg-background-dark font-display text-[#111318] dark:text-white">
          <div className="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden">
            <div className="layout-container flex h-full grow flex-col">
              <div className="flex flex-1 justify-center">
                <div className="layout-content-container flex flex-col max-w-[960px] flex-1 w-full">
                  <NewNavbar />
                  
                  <main className="mt-16 md:mt-20 min-h-screen">
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
                      
                      {/* Teacher-specific Routes */}
                      <Route path="/teacher/students" element={
                        <ProtectedRoute requiredRole="teacher">
                          <StudentsPage />
                        </ProtectedRoute>
                      } />
                      
                      <Route path="/teacher/create-groups" element={
                        <ProtectedRoute requiredRole="teacher">
                          <CreateGroupsPage />
                        </ProtectedRoute>
                      } />
                      
                      <Route path="/teacher/feedback" element={
                        <ProtectedRoute requiredRole="teacher">
                          <ViewFeedbackPage />
                        </ProtectedRoute>
                      } />
                      
                      {/* Admin-specific Routes */}
                      <Route path="/admin" element={
                        <ProtectedRoute requiredRole="admin">
                          <AdminPanel />
                        </ProtectedRoute>
                      } />
                      
                      <Route path="/admin/:section" element={
                        <ProtectedRoute requiredRole="admin">
                          <AdminPanel />
                        </ProtectedRoute>
                      } />
                      
                      {/* 404 Page */}
                      <Route path="*" element={<div className="text-center py-20">Page Not Found</div>} />
                    </Routes>
                  </main>
                  
                  <footer className="border-t border-solid border-b-[#f0f1f4]/10 dark:border-b-[#f0f1f4]/10 px-10 py-6 flex justify-between items-center text-sm">
                    <p className="text-[#616b89] dark:text-white/70">© 2024 Intelligent Peer Matchmaking. All rights reserved.</p>
                    <div className="flex gap-4">
                      <a className="text-[#616b89] dark:text-white/70 hover:text-primary dark:hover:text-primary" href="#">Privacy Policy</a>
                      <a className="text-[#616b89] dark:text-white/70 hover:text-primary dark:hover:text-primary" href="#">Terms of Service</a>
                    </div>
                  </footer>
                </div>
              </div>
            </div>
            
            {/* Chat Button */}
            <div className="fixed bottom-5 right-5 z-20">
              <button className="w-14 h-14 rounded-full bg-primary text-white flex items-center justify-center shadow-lg hover:bg-primary/90 transition-colors">
                <span className="material-symbols-outlined">chat_bubble</span>
              </button>
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
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;