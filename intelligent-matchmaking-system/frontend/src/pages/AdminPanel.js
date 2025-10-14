import React from 'react';
import { motion } from 'framer-motion';
import { ChartBarIcon, UsersIcon, CogIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';
import { Link } from 'react-router-dom';
import GlassButton from '../components/ui/GlassButton';

const AdminPanel = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-white p-6 space-y-8">
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">
          <span className="bg-gradient-to-r from-amber-500 to-amber-700 bg-clip-text text-transparent">
            Admin Panel
          </span>
        </h1>
        <p className="text-xl text-gray-600">
          System management and administration
        </p>
      </motion.div>
      
      <div className="grid md:grid-cols-3 gap-6">
        <GlassCard>
          <div className="p-6 text-center">
            <UsersIcon className="w-12 h-12 mx-auto mb-4 text-amber-500" />
            <h2 className="text-xl font-bold text-black mb-2">User Management</h2>
            <p className="text-gray-600 mb-4">
              Manage user accounts, roles, and permissions
            </p>
            <Link to="/admin/users">
              <GlassButton variant="primary" className="w-full">
                Manage Users
              </GlassButton>
            </Link>
          </div>
        </GlassCard>
        
        <GlassCard>
          <div className="p-6 text-center">
            <ChartBarIcon className="w-12 h-12 mx-auto mb-4 text-amber-500" />
            <h2 className="text-xl font-bold text-black mb-2">Analytics</h2>
            <p className="text-gray-600 mb-4">
              View platform usage and performance metrics
            </p>
            <Link to="/admin/analytics">
              <GlassButton variant="secondary" className="w-full">
                View Analytics
              </GlassButton>
            </Link>
          </div>
        </GlassCard>
        
        <GlassCard>
          <div className="p-6 text-center">
            <CogIcon className="w-12 h-12 mx-auto mb-4 text-amber-500" />
            <h2 className="text-xl font-bold text-black mb-2">System Settings</h2>
            <p className="text-gray-600 mb-4">
              Configure platform settings and preferences
            </p>
            <Link to="/admin/settings">
              <GlassButton variant="accent" className="w-full">
                System Settings
              </GlassButton>
            </Link>
          </div>
        </GlassCard>
      </div>
      
      <div className="max-w-4xl mx-auto mt-8">
        <GlassCard>
          <div className="p-6 text-center">
            <h2 className="text-2xl font-bold text-black mb-2">Admin-Only View</h2>
            <p className="text-gray-600">
              This page is only accessible to administrators. Here you have access to
              all system settings, user management, and analytics tools.
            </p>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default AdminPanel;