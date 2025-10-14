import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  // Render dashboard based on user role
  const renderDashboardByRole = () => {
    switch(user?.role) {
      case 'teacher':
        return renderTeacherDashboard();
      case 'admin':
        return renderAdminDashboard();
      default:
        return renderStudentDashboard();
    }
  };

  // Student Dashboard
  const renderStudentDashboard = () => {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">Welcome, {user?.full_name || 'Student'}!</h1>
          <p className="text-[#616b89] dark:text-white/70">
            Here's your personalized dashboard with matches and recommendations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Your Matches</h2>
              <span className="material-symbols-outlined text-primary">people</span>
            </div>
            <div className="space-y-4">
              {[1, 2, 3].map((item) => (
                <div key={item} className="flex items-center gap-3 p-3 rounded-lg bg-white/50 dark:bg-black/20">
                  <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
                    <span className="material-symbols-outlined">person</span>
                  </div>
                  <div>
                    <h3 className="font-medium">Match #{item}</h3>
                    <p className="text-sm text-[#616b89] dark:text-white/70">95% Compatibility</p>
                  </div>
                  <button className="ml-auto bg-primary/10 text-primary p-1 rounded-full">
                    <span className="material-symbols-outlined">arrow_forward</span>
                  </button>
                </div>
              ))}
              <Link to="/matches" className="block w-full py-2 text-center text-primary text-sm hover:underline">View All Matches</Link>
            </div>
          </div>

          <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Upcoming Sessions</h2>
              <span className="material-symbols-outlined text-primary">calendar_today</span>
            </div>
            <div className="space-y-4">
              {[1, 2].map((item) => (
                <div key={item} className="flex items-center gap-3 p-3 rounded-lg bg-white/50 dark:bg-black/20">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined">videocam</span>
                  </div>
                  <div>
                    <h3 className="font-medium">Study Session #{item}</h3>
                    <p className="text-sm text-[#616b89] dark:text-white/70">Tomorrow, 4:00 PM</p>
                  </div>
                  <button className="ml-auto bg-primary text-white p-1 rounded-full">
                    <span className="material-symbols-outlined">login</span>
                  </button>
                </div>
              ))}
              <button className="w-full py-2 text-primary text-sm hover:underline">Schedule New Session</button>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">Recommended Learning Paths</h2>
            <span className="material-symbols-outlined text-primary">auto_graph</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {['Web Development', 'Data Science', 'Mobile App Development'].map((path) => (
              <div key={path} className="flex flex-col gap-2 p-4 rounded-lg bg-white/50 dark:bg-black/20 hover:border-primary/50 dark:hover:border-primary/50 transition-all duration-300 transform hover:-translate-y-1 border border-transparent">
                <h3 className="font-medium">{path}</h3>
                <p className="text-sm text-[#616b89] dark:text-white/70">
                  Based on your interests and goals
                </p>
                <button className="mt-auto flex items-center text-primary text-sm">
                  View Path
                  <span className="material-symbols-outlined ml-1">arrow_forward</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Teacher Dashboard
  const renderTeacherDashboard = () => {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">Welcome, Professor {user?.full_name || 'Teacher'}!</h1>
          <p className="text-[#616b89] dark:text-white/70">
            Monitor your classes, create groups, and view student feedback.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/teacher/students" className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md hover:shadow-lg transition-all">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">My Students</h2>
              <span className="material-symbols-outlined text-purple-500">school</span>
            </div>
            <p className="text-[#616b89] dark:text-white/70 text-sm">View and manage your student roster</p>
            <div className="mt-2 flex justify-end">
              <span className="text-purple-500 text-sm flex items-center">
                View Students
                <span className="material-symbols-outlined ml-1">arrow_forward</span>
              </span>
            </div>
          </Link>

          <Link to="/teacher/create-groups" className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md hover:shadow-lg transition-all">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Create Groups</h2>
              <span className="material-symbols-outlined text-purple-500">group_add</span>
            </div>
            <p className="text-[#616b89] dark:text-white/70 text-sm">Form effective study groups based on student profiles</p>
            <div className="mt-2 flex justify-end">
              <span className="text-purple-500 text-sm flex items-center">
                Create Groups
                <span className="material-symbols-outlined ml-1">arrow_forward</span>
              </span>
            </div>
          </Link>

          <Link to="/teacher/feedback" className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md hover:shadow-lg transition-all">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Student Feedback</h2>
              <span className="material-symbols-outlined text-purple-500">chat</span>
            </div>
            <p className="text-[#616b89] dark:text-white/70 text-sm">Review feedback and improve your teaching</p>
            <div className="mt-2 flex justify-end">
              <span className="text-purple-500 text-sm flex items-center">
                View Feedback
                <span className="material-symbols-outlined ml-1">arrow_forward</span>
              </span>
            </div>
          </Link>
        </div>

        <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">Recent Student Activity</h2>
            <span className="material-symbols-outlined text-purple-500">trending_up</span>
          </div>
          <div className="space-y-4">
            {[1, 2, 3, 4].map((item) => (
              <div key={item} className="flex items-center gap-3 p-3 rounded-lg bg-white/50 dark:bg-black/20">
                <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
                  <span className="material-symbols-outlined">person</span>
                </div>
                <div>
                  <h3 className="font-medium">Student #{item}</h3>
                  <p className="text-sm text-[#616b89] dark:text-white/70">Completed assignment #{item}</p>
                </div>
                <div className="ml-auto text-sm text-[#616b89] dark:text-white/70">
                  Today, 2:30 PM
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Admin Dashboard
  const renderAdminDashboard = () => {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">Admin Dashboard</h1>
          <p className="text-[#616b89] dark:text-white/70">
            System management and administration.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/admin/users" className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md hover:shadow-lg transition-all">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">User Management</h2>
              <span className="material-symbols-outlined text-amber-500">manage_accounts</span>
            </div>
            <p className="text-[#616b89] dark:text-white/70 text-sm">Manage user accounts, roles, and permissions</p>
            <div className="mt-2 flex justify-end">
              <span className="text-amber-500 text-sm flex items-center">
                Manage Users
                <span className="material-symbols-outlined ml-1">arrow_forward</span>
              </span>
            </div>
          </Link>

          <Link to="/admin/analytics" className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md hover:shadow-lg transition-all">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Analytics</h2>
              <span className="material-symbols-outlined text-amber-500">monitoring</span>
            </div>
            <p className="text-[#616b89] dark:text-white/70 text-sm">View platform usage and performance metrics</p>
            <div className="mt-2 flex justify-end">
              <span className="text-amber-500 text-sm flex items-center">
                View Analytics
                <span className="material-symbols-outlined ml-1">arrow_forward</span>
              </span>
            </div>
          </Link>

          <Link to="/admin/settings" className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md hover:shadow-lg transition-all">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">System Settings</h2>
              <span className="material-symbols-outlined text-amber-500">settings</span>
            </div>
            <p className="text-[#616b89] dark:text-white/70 text-sm">Configure platform settings and preferences</p>
            <div className="mt-2 flex justify-end">
              <span className="text-amber-500 text-sm flex items-center">
                Manage Settings
                <span className="material-symbols-outlined ml-1">arrow_forward</span>
              </span>
            </div>
          </Link>
        </div>

        <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">System Status</h2>
            <span className="material-symbols-outlined text-amber-500">speed</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-white/50 dark:bg-black/20">
              <h3 className="font-medium text-green-600">System Online</h3>
              <p className="text-sm text-[#616b89] dark:text-white/70">All systems operational</p>
            </div>
            <div className="p-4 rounded-lg bg-white/50 dark:bg-black/20">
              <h3 className="font-medium">Active Users</h3>
              <p className="text-sm text-[#616b89] dark:text-white/70">253 users online now</p>
            </div>
            <div className="p-4 rounded-lg bg-white/50 dark:bg-black/20">
              <h3 className="font-medium">Server Load</h3>
              <p className="text-sm text-[#616b89] dark:text-white/70">32% - Normal</p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="px-4 py-8">
      {renderDashboardByRole()}
    </div>
  );
};

export default Dashboard;