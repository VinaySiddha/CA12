import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  UsersIcon, 
  AcademicCapIcon, 
  BookOpenIcon, 
  ChartBarIcon,
  SparklesIcon,
  TrophyIcon,
  ClockIcon,
  FireIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';
import GlassButton from '../components/ui/GlassButton';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [upcomingSessions, setUpcomingSessions] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Simulate API calls with mock data
      setTimeout(() => {
        setStats({
          totalMatches: 12,
          studyHours: 45,
          completedSessions: 8,
          currentStreak: 5,
          points: user?.points || 1250,
          level: user?.level || 5,
          nextLevelPoints: 300,
        });

        setRecentActivity([
          {
            type: 'match',
            title: 'New match found',
            description: 'Connected with Sarah for Machine Learning study',
            time: '2 hours ago',
            icon: UsersIcon,
            color: 'text-primary-400',
          },
          {
            type: 'session',
            title: 'Study session completed',
            description: 'Data Structures review with Alex',
            time: '1 day ago',
            icon: AcademicCapIcon,
            color: 'text-accent-400',
          },
          {
            type: 'achievement',
            title: 'Badge earned',
            description: 'Collaborative Learner badge unlocked',
            time: '2 days ago',
            icon: TrophyIcon,
            color: 'text-yellow-400',
          },
          {
            type: 'resource',
            title: 'New resource added',
            description: 'Advanced React Concepts tutorial',
            time: '3 days ago',
            icon: BookOpenIcon,
            color: 'text-secondary-400',
          },
        ]);

        setUpcomingSessions([
          {
            id: 1,
            partner: 'Emily Chen',
            topic: 'Database Design',
            time: 'Today, 3:00 PM',
            duration: '90 minutes',
            type: 'one-on-one',
            avatar: '👩‍💻',
          },
          {
            id: 2,
            partner: 'Study Group: React Masters',
            topic: 'Advanced React Patterns',
            time: 'Tomorrow, 7:00 PM',
            duration: '120 minutes',
            type: 'group',
            avatar: '👥',
          },
          {
            id: 3,
            partner: 'Michael Torres',
            topic: 'Algorithm Analysis',
            time: 'Friday, 2:00 PM',
            duration: '60 minutes',
            type: 'one-on-one',
            avatar: '👨‍🎓',
          },
        ]);

        setRecommendations([
          {
            type: 'user',
            title: 'Perfect Match Found!',
            description: 'Jessica Wang - 95% compatibility for Machine Learning',
            action: 'Send Connection Request',
            image: '👩‍🔬',
          },
          {
            type: 'group',
            title: 'Join Study Group',
            description: 'Data Science Bootcamp - 3 members, active daily',
            action: 'Join Group',
            image: '📊',
          },
          {
            type: 'resource',
            title: 'Recommended Course',
            description: 'Advanced Python Programming - matches your interests',
            action: 'View Course',
            image: '🐍',
          },
        ]);

        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading your dashboard..." />
      </div>
    );
  }

  const StatCard = ({ icon: Icon, label, value, color, subtitle }) => (
    <GlassCard hover className="text-center">
      <Icon className={`w-8 h-8 mx-auto mb-3 ${color}`} />
      <div className="text-2xl font-bold text-black mb-1">{value}</div>
      <div className="text-gray-600 text-sm">{label}</div>
      {subtitle && (
        <div className="text-gray-500 text-xs mt-1">{subtitle}</div>
      )}
    </GlassCard>
  );

  const ActivityItem = ({ activity }) => (
    <motion.div
      className="flex items-start space-x-4 p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
      whileHover={{ x: 5 }}
    >
      <div className={`p-2 rounded-full bg-gray-100`}>
        <activity.icon className={`w-5 h-5 ${activity.color}`} />
      </div>
      <div className="flex-1">
        <h4 className="text-black font-medium">{activity.title}</h4>
        <p className="text-gray-600 text-sm">{activity.description}</p>
        <p className="text-gray-500 text-xs mt-1">{activity.time}</p>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-white p-6 space-y-8">
      {/* Welcome Header */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">
          Welcome back,{' '}
          <span className="text-primary-500">
            {user?.profile?.full_name?.split(' ')[0] || 'Learner'}
          </span>
          !
        </h1>
        <p className="text-xl text-gray-600">
          Ready to continue your learning journey?
        </p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        className="grid grid-cols-2 md:grid-cols-4 gap-6"
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: { staggerChildren: 0.1 }
          }
        }}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <StatCard
            icon={UsersIcon}
            label="Total Matches"
            value={stats.totalMatches}
            color="text-primary-400"
          />
        </motion.div>
        
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <StatCard
            icon={ClockIcon}
            label="Study Hours"
            value={`${stats.studyHours}h`}
            color="text-accent-400"
            subtitle="This month"
          />
        </motion.div>
        
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <StatCard
            icon={TrophyIcon}
            label="Level"
            value={stats.level}
            color="text-yellow-400"
            subtitle={`${stats.points} points`}
          />
        </motion.div>
        
        <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
          <StatCard
            icon={FireIcon}
            label="Streak"
            value={`${stats.currentStreak} days`}
            color="text-red-400"
          />
        </motion.div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Upcoming Sessions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <GlassCard>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-black">Upcoming Sessions</h2>
                <GlassButton size="sm" variant="ghost">
                  View All
                </GlassButton>
              </div>
              
              <div className="space-y-4">
                {upcomingSessions.map((session) => (
                  <motion.div
                    key={session.id}
                    className="flex items-center justify-between p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-all group"
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className="flex items-center space-x-4">
                      <div className="text-2xl">{session.avatar}</div>
                      <div>
                        <h4 className="text-black font-medium">{session.partner}</h4>
                        <p className="text-gray-600 text-sm">{session.topic}</p>
                        <p className="text-gray-500 text-xs">{session.time} • {session.duration}</p>
                      </div>
                    </div>
                    <GlassButton size="sm" variant="primary">
                      Join
                    </GlassButton>
                  </motion.div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <GlassCard>
              <h2 className="text-2xl font-bold text-black mb-6">Recent Activity</h2>
              <div className="space-y-3">
                {recentActivity.map((activity, index) => (
                  <ActivityItem key={index} activity={activity} />
                ))}
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Progress Card */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <GlassCard glow>
              <div className="text-center">
                <div className="w-20 h-20 mx-auto mb-4 relative">
                  <svg className="w-20 h-20 transform -rotate-90">
                    <circle
                      cx="40"
                      cy="40"
                      r="32"
                      stroke="rgba(0,0,0,0.1)"
                      strokeWidth="6"
                      fill="transparent"
                    />
                    <circle
                      cx="40"
                      cy="40"
                      r="32"
                      stroke="url(#progressGradient)"
                      strokeWidth="6"
                      fill="transparent"
                      strokeDasharray={`${2 * Math.PI * 32}`}
                      strokeDashoffset={`${2 * Math.PI * 32 * (1 - (stats.points % 500) / 500)}`}
                      className="transition-all duration-1000"
                    />
                    <defs>
                      <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#3b82f6" />
                        <stop offset="100%" stopColor="#8b5cf6" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-black font-bold text-sm">
                      {Math.round((stats.points % 500) / 500 * 100)}%
                    </span>
                  </div>
                </div>
                
                <h3 className="text-lg font-semibold text-black mb-2">
                  Level {stats.level} Progress
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  {stats.nextLevelPoints} points to next level
                </p>
                
                <div className="grid grid-cols-2 gap-3 text-center">
                  <div>
                    <div className="text-2xl font-bold text-primary-500">{stats.points}</div>
                    <div className="text-gray-500 text-xs">Total Points</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-gray-700">{stats.completedSessions}</div>
                    <div className="text-gray-500 text-xs">Sessions</div>
                  </div>
                </div>
              </div>
            </GlassCard>
          </motion.div>

          {/* Recommendations */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <GlassCard>
              <h2 className="text-xl font-bold text-black mb-4">Recommendations</h2>
              <div className="space-y-3">
                {recommendations.map((rec, index) => (
                  <motion.div
                    key={index}
                    className="p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-all"
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className="flex items-start space-x-3">
                      <span className="text-2xl">{rec.image}</span>
                      <div className="flex-1">
                        <h4 className="text-black font-medium text-sm">{rec.title}</h4>
                        <p className="text-gray-600 text-xs mb-2">{rec.description}</p>
                        <GlassButton size="xs" variant="primary">
                          {rec.action}
                        </GlassButton>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <GlassCard>
              <h2 className="text-xl font-bold text-white mb-4">Quick Actions</h2>
              <div className="space-y-3">
                <GlassButton variant="primary" className="w-full justify-center">
                  <UsersIcon className="w-5 h-5 mr-2" />
                  Find Study Partners
                </GlassButton>
                <GlassButton variant="secondary" className="w-full justify-center">
                  <AcademicCapIcon className="w-5 h-5 mr-2" />
                  Join Study Group
                </GlassButton>
                <GlassButton variant="accent" className="w-full justify-center">
                  <BookOpenIcon className="w-5 h-5 mr-2" />
                  Browse Resources
                </GlassButton>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;