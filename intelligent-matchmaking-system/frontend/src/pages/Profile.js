import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  UserIcon,
  AcademicCapIcon,
  MapPinIcon,
  ClockIcon,
  StarIcon,
  TrophyIcon,
  BookOpenIcon,
  UsersIcon,
  CogIcon,
  CameraIcon,
  PencilIcon,
  CheckIcon,
  XMarkIcon,
  PlusIcon,
  FireIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';
import GlassButton from '../components/ui/GlassButton';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    full_name: '',
    bio: '',
    university: '',
    major: '',
    year: '',
    location: '',
    interests: [],
    skills: [],
    studyPreferences: {
      style: '',
      schedule: '',
      duration: '',
      subjects: []
    }
  });
  const [stats, setStats] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user?.profile) {
      setProfileData({
        full_name: user.profile.full_name || '',
        bio: user.profile.bio || '',
        university: user.profile.university || '',
        major: user.profile.major || '',
        year: user.profile.year || '',
        location: user.profile.location || '',
        interests: user.profile.interests || [],
        skills: user.profile.skills || [],
        studyPreferences: user.profile.studyPreferences || {
          style: '',
          schedule: '',
          duration: '',
          subjects: []
        }
      });
    }
    fetchProfileData();
  }, [user]);

  const fetchProfileData = async () => {
    try {
      setLoading(true);
      
      // Simulate API call with mock data
      setTimeout(() => {
        setStats({
          level: user?.level || 5,
          points: user?.points || 1250,
          nextLevelPoints: 300,
          studyHours: 45,
          connectionsCount: 12,
          groupsCount: 3,
          completedSessions: 23,
          currentStreak: 7,
          totalStreak: 15,
          rating: 4.8,
          reviewsCount: 34
        });

        setAchievements([
          {
            id: 1,
            title: 'Study Streak Master',
            description: 'Maintained a 7-day study streak',
            icon: '🔥',
            earnedDate: '2024-01-20',
            rarity: 'common'
          },
          {
            id: 2,
            title: 'Collaborative Learner',
            description: 'Completed 20+ study sessions with peers',
            icon: '🤝',
            earnedDate: '2024-01-18',
            rarity: 'rare'
          },
          {
            id: 3,
            title: 'Knowledge Sharer',
            description: 'Helped 10+ students with their studies',
            icon: '💡',
            earnedDate: '2024-01-15',
            rarity: 'epic'
          },
          {
            id: 4,
            title: 'Early Bird',
            description: 'Joined the platform in its first month',
            icon: '🐦',
            earnedDate: '2024-01-01',
            rarity: 'legendary'
          }
        ]);

        setRecentActivity([
          {
            type: 'session',
            title: 'Completed study session',
            description: 'Machine Learning fundamentals with Sarah',
            time: '2 hours ago'
          },
          {
            type: 'connection',
            title: 'New connection',
            description: 'Connected with Alex for Data Science',
            time: '1 day ago'
          },
          {
            type: 'achievement',
            title: 'Achievement unlocked',
            description: 'Study Streak Master badge earned',
            time: '2 days ago'
          },
          {
            type: 'group',
            title: 'Joined study group',
            description: 'React Developers United',
            time: '3 days ago'
          }
        ]);

        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching profile data:', error);
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      
      const result = await updateUser(profileData);
      if (result.success) {
        setIsEditing(false);
        toast.success('Profile updated successfully');
      } else {
        toast.error('Failed to update profile');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      toast.error('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    // Reset to original data
    if (user?.profile) {
      setProfileData({
        full_name: user.profile.full_name || '',
        bio: user.profile.bio || '',
        university: user.profile.university || '',
        major: user.profile.major || '',
        year: user.profile.year || '',
        location: user.profile.location || '',
        interests: user.profile.interests || [],
        skills: user.profile.skills || [],
        studyPreferences: user.profile.studyPreferences || {
          style: '',
          schedule: '',
          duration: '',
          subjects: []
        }
      });
    }
    setIsEditing(false);
  };

  const addTag = (type, value) => {
    if (value && !profileData[type].includes(value)) {
      setProfileData({
        ...profileData,
        [type]: [...profileData[type], value]
      });
    }
  };

  const removeTag = (type, index) => {
    setProfileData({
      ...profileData,
      [type]: profileData[type].filter((_, i) => i !== index)
    });
  };

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'common': return 'text-gray-400 border-gray-400/30';
      case 'rare': return 'text-blue-400 border-blue-400/30';
      case 'epic': return 'text-purple-400 border-purple-400/30';
      case 'legendary': return 'text-yellow-400 border-yellow-400/30';
      default: return 'text-gray-400 border-gray-400/30';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading your profile..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white p-6 space-y-8">
      {/* Header */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">
          Your{' '}
          <span className="text-primary">
            Profile
          </span>
        </h1>
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column - Profile Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Info */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <GlassCard>
              <div className="flex items-start justify-between mb-6">
                <h2 className="text-2xl font-bold text-black">Profile Information</h2>
                {!isEditing ? (
                  <GlassButton
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsEditing(true)}
                  >
                    <PencilIcon className="w-4 h-4 mr-2" />
                    Edit
                  </GlassButton>
                ) : (
                  <div className="flex space-x-2">
                    <GlassButton
                      variant="ghost"
                      size="sm"
                      onClick={handleCancel}
                      disabled={saving}
                    >
                      <XMarkIcon className="w-4 h-4 mr-2" />
                      Cancel
                    </GlassButton>
                    <GlassButton
                      variant="primary"
                      size="sm"
                      onClick={handleSave}
                      disabled={saving}
                    >
                      {saving ? (
                        <LoadingSpinner size="xs" />
                      ) : (
                        <>
                          <CheckIcon className="w-4 h-4 mr-2" />
                          Save
                        </>
                      )}
                    </GlassButton>
                  </div>
                )}
              </div>

              {/* Profile Picture */}
              <div className="flex items-center space-x-6 mb-6">
                <div className="relative">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary-400 to-secondary-400 flex items-center justify-center text-black text-3xl font-bold">
                    {profileData.full_name?.charAt(0) || user?.email?.charAt(0)?.toUpperCase() || 'U'}
                  </div>
                  {isEditing && (
                    <button className="absolute bottom-0 right-0 p-2 bg-primary-500 rounded-full text-black hover:bg-primary-600 transition-colors">
                      <CameraIcon className="w-4 h-4" />
                    </button>
                  )}
                </div>
                
                <div className="flex-1">
                  {isEditing ? (
                    <input
                      type="text"
                      value={profileData.full_name}
                      onChange={(e) => setProfileData({ ...profileData, full_name: e.target.value })}
                      className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-gray-500 focus:outline-none focus:border-primary-400 text-lg font-semibold"
                      placeholder="Full Name"
                    />
                  ) : (
                    <h3 className="text-2xl font-bold text-black">
                      {profileData.full_name || 'Your Name'}
                    </h3>
                  )}
                  <p className="text-gray-600 mt-1">{user?.email}</p>
                </div>
              </div>

              {/* Bio */}
              <div className="mb-6">
                <label className="block text-gray-600 text-sm mb-2">Bio</label>
                {isEditing ? (
                  <textarea
                    value={profileData.bio}
                    onChange={(e) => setProfileData({ ...profileData, bio: e.target.value })}
                    rows="3"
                    className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-gray-500 focus:outline-none focus:border-primary-400 resize-none"
                    placeholder="Tell others about yourself..."
                  />
                ) : (
                  <p className="text-gray-700">
                    {profileData.bio || 'No bio provided yet.'}
                  </p>
                )}
              </div>

              {/* Academic Info */}
              <div className="grid md:grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-gray-600 text-sm mb-2">University</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={profileData.university}
                      onChange={(e) => setProfileData({ ...profileData, university: e.target.value })}
                      className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-gray-500 focus:outline-none focus:border-primary-400"
                      placeholder="University name"
                    />
                  ) : (
                    <p className="text-gray-700 flex items-center">
                      <AcademicCapIcon className="w-4 h-4 mr-2" />
                      {profileData.university || 'Not specified'}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-gray-600 text-sm mb-2">Major</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={profileData.major}
                      onChange={(e) => setProfileData({ ...profileData, major: e.target.value })}
                      className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-gray-500 focus:outline-none focus:border-primary-400"
                      placeholder="Your major"
                    />
                  ) : (
                    <p className="text-gray-700 flex items-center">
                      <BookOpenIcon className="w-4 h-4 mr-2" />
                      {profileData.major || 'Not specified'}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-gray-600 text-sm mb-2">Academic Year</label>
                  {isEditing ? (
                    <select
                      value={profileData.year}
                      onChange={(e) => setProfileData({ ...profileData, year: e.target.value })}
                      className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400"
                    >
                      <option value="">Select year</option>
                      <option value="Freshman">Freshman</option>
                      <option value="Sophomore">Sophomore</option>
                      <option value="Junior">Junior</option>
                      <option value="Senior">Senior</option>
                      <option value="Graduate">Graduate</option>
                    </select>
                  ) : (
                    <p className="text-gray-700">
                      {profileData.year || 'Not specified'}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-gray-600 text-sm mb-2">Location</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={profileData.location}
                      onChange={(e) => setProfileData({ ...profileData, location: e.target.value })}
                      className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-gray-500 focus:outline-none focus:border-primary-400"
                      placeholder="City, State"
                    />
                  ) : (
                    <p className="text-gray-700 flex items-center">
                      <MapPinIcon className="w-4 h-4 mr-2" />
                      {profileData.location || 'Not specified'}
                    </p>
                  )}
                </div>
              </div>

              {/* Interests */}
              <div className="mb-6">
                <label className="block text-gray-600 text-sm mb-2">Interests</label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {profileData.interests.map((interest, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 rounded-full bg-primary/20 text-primary text-sm border border-primary/30 flex items-center"
                    >
                      {interest}
                      {isEditing && (
                        <button
                          onClick={() => removeTag('interests', index)}
                          className="ml-2 text-primary hover:text-black"
                        >
                          <XMarkIcon className="w-3 h-3" />
                        </button>
                      )}
                    </span>
                  ))}
                  {isEditing && (
                    <button
                      onClick={() => {
                        const interest = prompt('Add interest:');
                        if (interest) addTag('interests', interest);
                      }}
                      className="px-3 py-1 rounded-full bg-gray-100 text-gray-600 text-sm border border-gray-300 hover:bg-white/20 transition-colors flex items-center"
                    >
                      <PlusIcon className="w-3 h-3 mr-1" />
                      Add
                    </button>
                  )}
                </div>
              </div>

              {/* Skills */}
              <div>
                <label className="block text-gray-600 text-sm mb-2">Skills</label>
                <div className="flex flex-wrap gap-2">
                  {profileData.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 rounded-full bg-secondary-500/20 text-secondary-300 text-sm border border-secondary-400/30 flex items-center"
                    >
                      {skill}
                      {isEditing && (
                        <button
                          onClick={() => removeTag('skills', index)}
                          className="ml-2 text-secondary-300 hover:text-black"
                        >
                          <XMarkIcon className="w-3 h-3" />
                        </button>
                      )}
                    </span>
                  ))}
                  {isEditing && (
                    <button
                      onClick={() => {
                        const skill = prompt('Add skill:');
                        if (skill) addTag('skills', skill);
                      }}
                      className="px-3 py-1 rounded-full bg-gray-100 text-gray-600 text-sm border border-gray-300 hover:bg-white/20 transition-colors flex items-center"
                    >
                      <PlusIcon className="w-3 h-3 mr-1" />
                      Add
                    </button>
                  )}
                </div>
              </div>
            </GlassCard>
          </motion.div>

          {/* Achievements */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <GlassCard>
              <h2 className="text-2xl font-bold text-black mb-6">Achievements</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {achievements.map((achievement) => (
                  <div
                    key={achievement.id}
                    className={`p-4 rounded-lg border ${getRarityColor(achievement.rarity)} bg-gray-50 hover:bg-gray-100 transition-colors`}
                  >
                    <div className="flex items-start space-x-3">
                      <span className="text-3xl">{achievement.icon}</span>
                      <div className="flex-1">
                        <h4 className="text-black font-semibold">{achievement.title}</h4>
                        <p className="text-gray-600 text-sm">{achievement.description}</p>
                        <p className="text-gray-500 text-xs mt-1">
                          Earned on {new Date(achievement.earnedDate).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <GlassCard>
              <h2 className="text-2xl font-bold text-black mb-6">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-4 p-3 rounded-lg bg-gray-50">
                    <div className="p-2 rounded-full bg-gray-100">
                      {activity.type === 'session' && <ClockIcon className="w-4 h-4 text-blue-400" />}
                      {activity.type === 'connection' && <UsersIcon className="w-4 h-4 text-green-400" />}
                      {activity.type === 'achievement' && <TrophyIcon className="w-4 h-4 text-yellow-400" />}
                      {activity.type === 'group' && <AcademicCapIcon className="w-4 h-4 text-purple-400" />}
                    </div>
                    <div className="flex-1">
                      <h4 className="text-black font-medium">{activity.title}</h4>
                      <p className="text-gray-600 text-sm">{activity.description}</p>
                      <p className="text-gray-500 text-xs mt-1">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </motion.div>
        </div>

        {/* Right Column - Stats */}
        <div className="space-y-6">
          {/* Level Progress */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <GlassCard glow>
              <div className="text-center">
                <div className="w-20 h-20 mx-auto mb-4 relative">
                  <svg className="w-20 h-20 transform -rotate-90">
                    <circle
                      cx="40"
                      cy="40"
                      r="32"
                      stroke="rgba(255,255,255,0.2)"
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
                    <span className="text-black font-bold text-lg">{stats.level}</span>
                  </div>
                </div>
                
                <h3 className="text-lg font-semibold text-black mb-2">
                  Level {stats.level}
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  {stats.nextLevelPoints} points to next level
                </p>
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{stats.points}</div>
                  <div className="text-gray-500 text-sm">Total Points</div>
                </div>
              </div>
            </GlassCard>
          </motion.div>

          {/* Stats Grid */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <GlassCard>
              <h3 className="text-lg font-semibold text-black mb-4">Statistics</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 flex items-center">
                    <ClockIcon className="w-4 h-4 mr-2" />
                    Study Hours
                  </span>
                  <span className="text-black font-semibold">{stats.studyHours}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 flex items-center">
                    <UsersIcon className="w-4 h-4 mr-2" />
                    Connections
                  </span>
                  <span className="text-black font-semibold">{stats.connectionsCount}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 flex items-center">
                    <AcademicCapIcon className="w-4 h-4 mr-2" />
                    Study Groups
                  </span>
                  <span className="text-black font-semibold">{stats.groupsCount}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 flex items-center">
                    <CheckIcon className="w-4 h-4 mr-2" />
                    Sessions Completed
                  </span>
                  <span className="text-black font-semibold">{stats.completedSessions}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 flex items-center">
                    <FireIcon className="w-4 h-4 mr-2" />
                    Current Streak
                  </span>
                  <span className="text-orange-400 font-semibold">{stats.currentStreak} days</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 flex items-center">
                    <StarIcon className="w-4 h-4 mr-2" />
                    Rating
                  </span>
                  <span className="text-yellow-400 font-semibold">
                    {stats.rating} ({stats.reviewsCount} reviews)
                  </span>
                </div>
              </div>
            </GlassCard>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <GlassCard>
              <h3 className="text-lg font-semibold text-black mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <GlassButton variant="primary" className="w-full justify-center">
                  <UsersIcon className="w-4 h-4 mr-2" />
                  Find Study Partners
                </GlassButton>
                <GlassButton variant="secondary" className="w-full justify-center">
                  <AcademicCapIcon className="w-4 h-4 mr-2" />
                  Join Study Group
                </GlassButton>
                <GlassButton variant="accent" className="w-full justify-center">
                  <BookOpenIcon className="w-4 h-4 mr-2" />
                  Browse Resources
                </GlassButton>
                <GlassButton variant="ghost" className="w-full justify-center">
                  <CogIcon className="w-4 h-4 mr-2" />
                  Settings
                </GlassButton>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Profile;