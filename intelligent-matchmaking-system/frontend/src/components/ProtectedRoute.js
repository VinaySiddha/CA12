import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from './ui/LoadingSpinner';
import toast from 'react-hot-toast';

const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, user, loading } = useAuth();
  const location = useLocation();

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check role-based access
  if (requiredRole) {
    // Handle array of roles
    if (Array.isArray(requiredRole)) {
      if (!user?.role || !requiredRole.includes(user.role)) {
        toast.error(`Access denied. Requires one of these roles: ${requiredRole.join(', ')}`);
        return <Navigate to="/dashboard" replace />;
      }
    } 
    // Handle single role
    else if (!user?.role || user.role !== requiredRole) {
      toast.error(`Access denied. Requires ${requiredRole} role.`);
      return <Navigate to="/dashboard" replace />;
    }
  }

  return children;
};

export default ProtectedRoute;