import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  UsersIcon,
  PlusIcon,
  ChatBubbleLeftRightIcon,
  CalendarIcon,
  ClockIcon,
  MapPinIcon,
  UserPlusIcon,
  CogIcon,
  MagnifyingGlassIcon,
  AcademicCapIcon,
  SparklesIcon,
  VideoCameraIcon,
  BookOpenIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';
import GlassButton from '../components/ui/GlassButton';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const StudyGroups = () => {
  const { user } = useAuth();
  const [studyGroups, setStudyGroups] = useState([]);
  const [myGroups, setMyGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [activeTab, setActiveTab] = useState('discover'); // discover, my-groups
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    subject: '',
    size: '',
    schedule: '',
    level: ''
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStudyGroups();
  }, [activeTab, searchQuery, filters]);

  const fetchStudyGroups = async () => {
    try {
      setLoading(true);
      
      // Fetch real study groups from API
      const response = await fetch('http://localhost:8000/matches/study-groups', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch study groups');
      }
      
      const data = await response.json();
      
      if (activeTab === 'discover') {
        setStudyGroups(data);
      } else if (activeTab === 'my-groups') {
        // Filter groups where user is a member
        const myGroupsData = data.filter(group => 
          group.members.some(member => member.user_id === user?.id)
        );
        setMyGroups(myGroupsData);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching study groups:', error);
      setLoading(false);
      // Fallback to empty array if API fails
      setStudyGroups([]);
      setMyGroups([]);
    }
  };
          {
            id: 1,
            name: 'AI/ML Study Circle',
            description: 'Deep dive into machine learning algorithms, neural networks, and practical AI applications. We work on projects and share research papers.',
            subject: 'Machine Learning',
            level: 'Advanced',
            members: [
              { id: 1, name: 'Sarah Chen', avatar: '👩‍💻', role: 'admin' },
              { id: 2, name: 'Alex Kim', avatar: '👨‍🎓', role: 'member' },
              { id: 3, name: 'Maya Patel', avatar: '👩‍🔬', role: 'member' },
              { id: 4, name: 'David Wu', avatar: '👨‍💼', role: 'member' }
            ],
            maxMembers: 8,
            schedule: {
              days: ['Tuesday', 'Thursday'],
              time: '7:00 PM',
              duration: '2 hours',
              timezone: 'EST'
            },
            location: 'Virtual (Zoom)',
            tags: ['Machine Learning', 'Deep Learning', 'Python', 'Research'],
            createdDate: '2024-01-15',
            lastActivity: '2 hours ago',
            upcomingSessions: [
              {
                date: '2024-01-25',
                time: '7:00 PM',
                topic: 'Convolutional Neural Networks',
                type: 'Discussion + Coding'
              },
              {
                date: '2024-01-27',
                time: '7:00 PM',
                topic: 'Project Presentations',
                type: 'Presentations'
              }
            ],
            requirements: 'Basic knowledge of Python and linear algebra',
            isPublic: true,
            rating: 4.8,
            sessionsCompleted: 24
          },
          {
            id: 2,
            name: 'React Developers United',
            description: 'Learn modern React patterns, hooks, and best practices. Build real-world projects together and review each other\'s code.',
            subject: 'Web Development',
            level: 'Intermediate',
            members: [
              { id: 5, name: 'Emily Zhang', avatar: '👩‍💻', role: 'admin' },
              { id: 6, name: 'Jordan Smith', avatar: '👨‍💻', role: 'moderator' },
              { id: 7, name: 'Lisa Wang', avatar: '👩‍🎨', role: 'member' },
              { id: 8, name: 'Carlos Rodriguez', avatar: '👨‍🔧', role: 'member' },
              { id: 9, name: 'Aisha Johnson', avatar: '👩‍💼', role: 'member' }
            ],
            maxMembers: 10,
            schedule: {
              days: ['Saturday'],
              time: '2:00 PM',
              duration: '3 hours',
              timezone: 'PST'
            },
            location: 'Stanford Library + Virtual',
            tags: ['React', 'JavaScript', 'Frontend', 'Project-based'],
            createdDate: '2024-01-10',
            lastActivity: '1 day ago',
            upcomingSessions: [
              {
                date: '2024-01-27',
                time: '2:00 PM',
                topic: 'Advanced React Hooks',
                type: 'Workshop'
              }
            ],
            requirements: 'Comfortable with JavaScript ES6+ and basic React',
            isPublic: true,
            rating: 4.9,
            sessionsCompleted: 18
          },
          {
            id: 3,
            name: 'Data Science Bootcamp',
            description: 'Comprehensive data science study group covering statistics, Python, R, and machine learning. Perfect for beginners.',
            subject: 'Data Science',
            level: 'Beginner',
            members: [
              { id: 10, name: 'Michael Torres', avatar: '👨‍🎓', role: 'admin' },
              { id: 11, name: 'Sophie Brown', avatar: '👩‍🔬', role: 'member' },
              { id: 12, name: 'Ryan O\'Connor', avatar: '👨‍💼', role: 'member' }
            ],
            maxMembers: 6,
            schedule: {
              days: ['Monday', 'Wednesday', 'Friday'],
              time: '6:00 PM',
              duration: '1.5 hours',
              timezone: 'EST'
            },
            location: 'Virtual (Discord)',
            tags: ['Data Science', 'Python', 'Statistics', 'Pandas'],
            createdDate: '2024-01-20',
            lastActivity: '5 hours ago',
            upcomingSessions: [
              {
                date: '2024-01-24',
                time: '6:00 PM',
                topic: 'Data Visualization with Matplotlib',
                type: 'Hands-on Session'
              }
            ],
            requirements: 'No prior experience needed',
            isPublic: true,
            rating: 4.7,
            sessionsCompleted: 12
          },
          {
            id: 4,
            name: 'Algorithms & Data Structures',
            description: 'Master fundamental algorithms and data structures. Practice coding problems and prepare for technical interviews.',
            subject: 'Computer Science',
            level: 'Intermediate',
            members: [
              { id: 13, name: 'Kevin Liu', avatar: '👨‍💻', role: 'admin' },
              { id: 14, name: 'Rachel Green', avatar: '👩‍🎓', role: 'member' },
              { id: 15, name: 'James Wilson', avatar: '👨‍🔬', role: 'member' },
              { id: 16, name: 'Nina Singh', avatar: '👩‍💻', role: 'member' },
              { id: 17, name: 'Tom Anderson', avatar: '👨‍🎓', role: 'member' },
              { id: 18, name: 'Maria Garcia', avatar: '👩‍🔧', role: 'member' }
            ],
            maxMembers: 8,
            schedule: {
              days: ['Sunday'],
              time: '10:00 AM',
              duration: '4 hours',
              timezone: 'PST'
            },
            location: 'UC Berkeley Campus',
            tags: ['Algorithms', 'Data Structures', 'Coding', 'Interview Prep'],
            createdDate: '2024-01-05',
            lastActivity: '3 days ago',
            upcomingSessions: [
              {
                date: '2024-01-28',
                time: '10:00 AM',
                topic: 'Dynamic Programming',
                type: 'Problem Solving'
              }
            ],
            requirements: 'Proficiency in at least one programming language',
            isPublic: true,
            rating: 4.6,
            sessionsCompleted: 20
          }
        ];

        if (activeTab === 'discover') {
          setStudyGroups(mockGroups);
        } else {
          // User's groups (they're member of first two groups)
          setMyGroups(mockGroups.slice(0, 2));
        }
        
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching study groups:', error);
      setLoading(false);
    }
  };

  const handleJoinGroup = (groupId) => {
    console.log('Joining group:', groupId);
    // Handle join group logic
  };

  const handleLeaveGroup = (groupId) => {
    console.log('Leaving group:', groupId);
    // Handle leave group logic
  };

  const GroupCard = ({ group, isJoined = false }) => (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ y: -5 }}
    >
      <GlassCard hover className="h-full">
        {/* Header */}
        <div className="p-6 pb-4">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h3 className="text-xl font-bold text-black mb-2">{group.name}</h3>
              <p className="text-gray-600 text-sm leading-relaxed">{group.description}</p>
            </div>
            <div className="ml-4">
              <div className="text-center">
                <div className="text-lg font-bold text-primary">{group.members.length}</div>
                <div className="text-black/60 text-xs">/{group.maxMembers}</div>
              </div>
            </div>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mb-4">
            {group.tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="px-2 py-1 rounded-full bg-gray-100 text-gray-700 text-xs border border-gray-300"
              >
                {tag}
              </span>
            ))}
            {group.tags.length > 3 && (
              <span className="px-2 py-1 rounded-full bg-gray-100 text-black/60 text-xs">
                +{group.tags.length - 3} more
              </span>
            )}
          </div>

          {/* Info Grid */}
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="flex items-center text-gray-600">
              <AcademicCapIcon className="w-4 h-4 mr-2" />
              {group.level}
            </div>
            <div className="flex items-center text-gray-600">
              <CalendarIcon className="w-4 h-4 mr-2" />
              {group.schedule.days.join(', ')}
            </div>
            <div className="flex items-center text-gray-600">
              <ClockIcon className="w-4 h-4 mr-2" />
              {group.schedule.time}
            </div>
            <div className="flex items-center text-gray-600">
              <MapPinIcon className="w-4 h-4 mr-2" />
              {group.location.includes('Virtual') ? '🌐' : '📍'} {group.location.split(' ')[0]}
            </div>
          </div>
        </div>

        {/* Members Preview */}
        <div className="px-6 pb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-600 text-sm">Members</span>
            <span className="text-gray-500 text-xs">{group.lastActivity}</span>
          </div>
          <div className="flex -space-x-2">
            {group.members.slice(0, 5).map((member, index) => (
              <div
                key={member.id}
                className="w-8 h-8 rounded-full bg-gray-100 border-2 border-gray-300 flex items-center justify-center text-sm relative group"
                title={member.name}
              >
                {member.avatar}
                {member.role === 'admin' && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-400 rounded-full border border-gray-300"></div>
                )}
              </div>
            ))}
            {group.members.length > 5 && (
              <div className="w-8 h-8 rounded-full bg-gray-100 border-2 border-gray-300 flex items-center justify-center text-xs text-black/60">
                +{group.members.length - 5}
              </div>
            )}
          </div>
        </div>

        {/* Next Session */}
        {group.upcomingSessions.length > 0 && (
          <div className="px-6 pb-4">
            <div className="p-3 rounded-lg bg-primary-500/20 border border-primary-400/30">
              <div className="text-primary text-sm font-medium mb-1">Next Session</div>
              <div className="text-black text-sm">{group.upcomingSessions[0].topic}</div>
              <div className="text-black/60 text-xs">
                {group.upcomingSessions[0].date} at {group.upcomingSessions[0].time}
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="px-6 pb-6 pt-2 flex space-x-3">
          <GlassButton
            variant="ghost"
            size="sm"
            onClick={() => setSelectedGroup(group)}
            className="flex-1"
          >
            View Details
          </GlassButton>
          
          {isJoined ? (
            <GlassButton
              variant="secondary"
              size="sm"
              onClick={() => handleLeaveGroup(group.id)}
            >
              <ChatBubbleLeftRightIcon className="w-4 h-4 mr-2" />
              Chat
            </GlassButton>
          ) : (
            <GlassButton
              variant="primary"
              size="sm"
              onClick={() => handleJoinGroup(group.id)}
              disabled={group.members.length >= group.maxMembers}
            >
              <UserPlusIcon className="w-4 h-4 mr-2" />
              {group.members.length >= group.maxMembers ? 'Full' : 'Join'}
            </GlassButton>
          )}
        </div>

        {/* Stats */}
        <div className="px-6 pb-4 pt-2 border-t border-white/10">
          <div className="flex justify-between text-xs text-black/60">
            <span>★ {group.rating} rating</span>
            <span>{group.sessionsCompleted} sessions completed</span>
          </div>
        </div>
      </GlassCard>
    </motion.div>
  );

  const CreateGroupModal = () => (
    <AnimatePresence>
      {showCreateModal && (
        <motion.div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setShowCreateModal(false)}
        >
          <motion.div
            className="bg-glass backdrop-blur-xl border border-gray-300 rounded-2xl p-6 max-w-lg w-full"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-2xl font-bold text-black mb-6">Create Study Group</h2>
            
            <form className="space-y-4">
              <div>
                <label className="block text-gray-600 text-sm mb-2">Group Name</label>
                <input
                  type="text"
                  className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-white/50 focus:outline-none focus:border-primary-400"
                  placeholder="Enter group name..."
                />
              </div>
              
              <div>
                <label className="block text-gray-600 text-sm mb-2">Description</label>
                <textarea
                  rows="3"
                  className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-white/50 focus:outline-none focus:border-primary-400 resize-none"
                  placeholder="Describe your study group..."
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-600 text-sm mb-2">Subject</label>
                  <select className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400">
                    <option value="">Select subject</option>
                    <option value="machine-learning">Machine Learning</option>
                    <option value="web-development">Web Development</option>
                    <option value="data-science">Data Science</option>
                    <option value="computer-science">Computer Science</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-gray-600 text-sm mb-2">Level</label>
                  <select className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400">
                    <option value="">Select level</option>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-600 text-sm mb-2">Max Members</label>
                  <input
                    type="number"
                    min="3"
                    max="20"
                    className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-white/50 focus:outline-none focus:border-primary-400"
                    placeholder="8"
                  />
                </div>
                
                <div>
                  <label className="block text-gray-600 text-sm mb-2">Location</label>
                  <select className="w-full p-3 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400">
                    <option value="virtual">Virtual</option>
                    <option value="hybrid">Hybrid</option>
                    <option value="in-person">In-person</option>
                  </select>
                </div>
              </div>
              
              <div className="flex space-x-3 pt-4">
                <GlassButton
                  type="button"
                  variant="ghost"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1"
                >
                  Cancel
                </GlassButton>
                <GlassButton
                  type="submit"
                  variant="primary"
                  className="flex-1"
                >
                  Create Group
                </GlassButton>
              </div>
            </form>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading study groups..." />
      </div>
    );
  }

  const currentGroups = activeTab === 'discover' ? studyGroups : myGroups;

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
          Join{' '}
          <span className="text-gradient bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
            Study Groups
          </span>
        </h1>
        <p className="text-xl text-gray-700">
          Learn together, achieve more - find your study community
        </p>
      </motion.div>

      {/* Tabs */}
      <motion.div
        className="flex justify-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="flex bg-gray-100 rounded-lg p-1 backdrop-blur-sm border border-gray-300">
          <button
            onClick={() => setActiveTab('discover')}
            className={`px-6 py-2 rounded-md transition-all ${
              activeTab === 'discover'
                ? 'bg-primary-500 text-black shadow-lg'
                : 'text-gray-600 hover:text-black'
            }`}
          >
            Discover Groups
          </button>
          <button
            onClick={() => setActiveTab('my-groups')}
            className={`px-6 py-2 rounded-md transition-all ${
              activeTab === 'my-groups'
                ? 'bg-primary-500 text-black shadow-lg'
                : 'text-gray-600 hover:text-black'
            }`}
          >
            My Groups
          </button>
        </div>
      </motion.div>

      {/* Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <GlassCard>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search study groups..."
                className="w-full pl-10 pr-4 py-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-white/50 focus:outline-none focus:border-primary-400"
              />
            </div>
            
            {/* Filters */}
            <div className="flex space-x-3">
              <select
                value={filters.subject}
                onChange={(e) => setFilters({ ...filters, subject: e.target.value })}
                className="p-2 rounded-lg bg-gray-100 border border-gray-300 text-black text-sm focus:outline-none focus:border-primary-400"
              >
                <option value="">All Subjects</option>
                <option value="machine-learning">Machine Learning</option>
                <option value="web-development">Web Development</option>
                <option value="data-science">Data Science</option>
                <option value="computer-science">Computer Science</option>
              </select>
              
              <GlassButton
                variant="primary"
                onClick={() => setShowCreateModal(true)}
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                Create Group
              </GlassButton>
            </div>
          </div>
        </GlassCard>
      </motion.div>

      {/* Groups Grid */}
      <motion.div
        className="grid md:grid-cols-2 xl:grid-cols-3 gap-6"
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
        <AnimatePresence>
          {currentGroups.map((group) => (
            <motion.div
              key={group.id}
              variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            >
              <GroupCard 
                group={group} 
                isJoined={activeTab === 'my-groups'} 
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>

      {/* Empty State */}
      {currentGroups.length === 0 && (
        <motion.div
          className="text-center py-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="text-6xl mb-4">📚</div>
          <h3 className="text-xl font-semibold text-black mb-2">
            {activeTab === 'discover' ? 'No groups found' : 'You haven\'t joined any groups yet'}
          </h3>
          <p className="text-gray-600 mb-6">
            {activeTab === 'discover' 
              ? 'Try adjusting your search or filters' 
              : 'Discover amazing study groups and start learning together'
            }
          </p>
          {activeTab === 'my-groups' && (
            <GlassButton
              variant="primary"
              onClick={() => setActiveTab('discover')}
            >
              <MagnifyingGlassIcon className="w-5 h-5 mr-2" />
              Discover Groups
            </GlassButton>
          )}
        </motion.div>
      )}

      {/* Create Group Modal */}
      <CreateGroupModal />
    </div>
  );
};

export default StudyGroups;