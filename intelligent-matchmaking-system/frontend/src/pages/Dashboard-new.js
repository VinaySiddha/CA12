import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import CreatePost from '../components/social/CreatePost';
import Post from '../components/social/Post';
import TeacherDashboard from './Dashboard-teacher';

const Dashboard = () => {
  const { user } = useAuth();
  const [posts, setPosts] = useState([]);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch posts and expert matches in parallel
      const [postsResponse, matchesResponse] = await Promise.all([
        axios.get('/social/posts?limit=10'),
        user?.role === 'student' 
          ? axios.get('/matches/expert-matches?limit=5')  // Get expert matches for students
          : axios.get('/matches/ml-recommendations?limit=5')  // Fallback for other roles
      ]);

      setPosts(postsResponse.data || []);
      setMatches(matchesResponse.data || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handlePostCreated = () => {
    fetchDashboardData();
  };

  const handlePostDeleted = (postId) => {
    setPosts(posts.filter(p => p.id !== postId));
  };

  // Show teacher dashboard for teachers and experts
  if (user?.role === 'teacher' || user?.role === 'expert') {
    return <TeacherDashboard />;
  }

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
            Connect, learn, and grow with your peers.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Feed */}
          <div className="lg:col-span-2 space-y-6">
            <CreatePost onPostCreated={handlePostCreated} />
            
            {loading ? (
              <div className="flex justify-center py-12">
                <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
              </div>
            ) : posts.length > 0 ? (
              <div className="space-y-6">
                {posts.map((post) => (
                  <Post key={post.id} post={post} onDelete={handlePostDeleted} />
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-12 text-center backdrop-blur-md">
                <span className="material-symbols-outlined text-6xl text-[#616b89] dark:text-white/70 mb-4">post_add</span>
                <h3 className="text-lg font-semibold mb-2">No posts yet</h3>
                <p className="text-[#616b89] dark:text-white/70">Be the first to share something!</p>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Expert Matches */}
            <div className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">psychology</span>
                  Expert Matches
                </h2>
              </div>
              <div className="space-y-3">
                {matches.length > 0 ? (
                  matches.map((match, index) => (
                    <div key={index} className="flex flex-col gap-2 p-4 rounded-lg bg-white/50 dark:bg-black/20 hover:bg-primary/5 transition-colors cursor-pointer border border-primary/20">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white font-bold">
                          {match.full_name?.charAt(0).toUpperCase() || 'E'}
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-sm">{match.full_name || 'Expert'}</h3>
                          <p className="text-xs text-[#616b89] dark:text-white/70">{match.job_title || match.role}</p>
                          {match.company && <p className="text-xs text-[#616b89] dark:text-white/70">@ {match.company}</p>}
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-bold text-primary">{(match.match_score * 100).toFixed(0)}%</div>
                          <div className="text-xs text-[#616b89] dark:text-white/70">Match</div>
                        </div>
                      </div>
                      
                      {/* Expertise Areas */}
                      {match.expertise_areas && match.expertise_areas.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {match.expertise_areas.slice(0, 3).map((area, i) => (
                            <span key={i} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">
                              {area}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      {/* Matched Interests */}
                      {match.matched_interests && match.matched_interests.length > 0 && (
                        <div className="flex items-center gap-1 mt-1 text-xs text-green-600 dark:text-green-400">
                          <span className="material-symbols-outlined text-sm">check_circle</span>
                          <span>{match.matched_interests.length} shared interests</span>
                        </div>
                      )}
                      
                      <button className="mt-2 w-full bg-primary/10 text-primary py-2 rounded-lg hover:bg-primary/20 transition-colors text-sm font-medium">
                        View Profile
                      </button>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-[#616b89] dark:text-white/70 text-center py-4">
                    {loading ? 'Finding experts...' : 'No expert matches found yet'}
                  </p>
                )}
                <Link to="/matches" className="block w-full py-2 text-center text-primary text-sm hover:underline">
                  View All Experts
                </Link>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
              <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
              <div className="space-y-2">
                <Link to="/study-groups" className="flex items-center gap-3 p-3 rounded-lg hover:bg-primary/5 transition-colors">
                  <span className="material-symbols-outlined text-primary">groups</span>
                  <span className="text-sm font-medium">Join Study Group</span>
                </Link>
                <Link to="/resources" className="flex items-center gap-3 p-3 rounded-lg hover:bg-primary/5 transition-colors">
                  <span className="material-symbols-outlined text-primary">library_books</span>
                  <span className="text-sm font-medium">Browse Resources</span>
                </Link>
                <Link to="/profile" className="flex items-center gap-3 p-3 rounded-lg hover:bg-primary/5 transition-colors">
                  <span className="material-symbols-outlined text-primary">account_circle</span>
                  <span className="text-sm font-medium">Edit Profile</span>
                </Link>
              </div>
            </div>
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