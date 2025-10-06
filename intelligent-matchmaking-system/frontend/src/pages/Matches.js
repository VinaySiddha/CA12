import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  HeartIcon,
  ChatBubbleLeftRightIcon,
  UserPlusIcon,
  XMarkIcon,
  InformationCircleIcon,
  SparklesIcon,
  AcademicCapIcon,
  CalendarIcon,
  MapPinIcon,
  ClockIcon,
  StarIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolid } from '@heroicons/react/24/solid';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';
import GlassButton from '../components/ui/GlassButton';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const Matches = () => {
  const { user } = useAuth();
  const [matches, setMatches] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [filterCriteria, setFilterCriteria] = useState({
    subject: '',
    skillLevel: '',
    studyStyle: '',
    availability: ''
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('discover'); // discover, connections, requests

  useEffect(() => {
    fetchMatches();
  }, [filterCriteria]);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      
      // Simulate API call with mock data
      setTimeout(() => {
        const mockMatches = [
          {
            id: 1,
            profile: {
              full_name: 'Sarah Chen',
              avatar: '👩‍💻',
              university: 'MIT',
              major: 'Computer Science',
              year: 'Junior',
              location: 'Cambridge, MA',
              bio: 'Passionate about machine learning and AI. Looking for study partners for advanced algorithms and data structures.',
              subjects: ['Machine Learning', 'Algorithms', 'Python', 'Data Structures'],
              skills: {
                'Machine Learning': 'Advanced',
                'Python': 'Expert',
                'Algorithms': 'Intermediate',
                'Data Structures': 'Advanced'
              },
              studyPreferences: {
                style: 'Visual learner',
                schedule: 'Evening',
                duration: '2-3 hours',
                frequency: '3x per week'
              },
              achievements: ['Top 10% in ML Course', 'Python Certification', 'Hackathon Winner'],
              rating: 4.9,
              completedSessions: 23,
              responseRate: '95%'
            },
            compatibility: 95,
            matchReason: 'Perfect match for Machine Learning study',
            sharedSubjects: ['Machine Learning', 'Python', 'Algorithms'],
            lastActive: '2 hours ago',
            status: 'online'
          },
          {
            id: 2,
            profile: {
              full_name: 'Alex Rodriguez',
              avatar: '👨‍🎓',
              university: 'Stanford',
              major: 'Data Science',
              year: 'Senior',
              location: 'Palo Alto, CA',
              bio: 'Data science enthusiast with experience in statistical analysis and visualization. Love collaborative problem-solving.',
              subjects: ['Statistics', 'R Programming', 'Data Visualization', 'Machine Learning'],
              skills: {
                'Statistics': 'Expert',
                'R Programming': 'Advanced',
                'Python': 'Intermediate',
                'Data Visualization': 'Advanced'
              },
              studyPreferences: {
                style: 'Hands-on learner',
                schedule: 'Afternoon',
                duration: '1-2 hours',
                frequency: '2x per week'
              },
              achievements: ['Statistics Excellence Award', 'Research Publication', 'TA Experience'],
              rating: 4.8,
              completedSessions: 31,
              responseRate: '92%'
            },
            compatibility: 87,
            matchReason: 'Strong overlap in data science interests',
            sharedSubjects: ['Statistics', 'Machine Learning', 'Python'],
            lastActive: '1 day ago',
            status: 'away'
          },
          {
            id: 3,
            profile: {
              full_name: 'Emily Zhang',
              avatar: '👩‍🔬',
              university: 'UC Berkeley',
              major: 'Software Engineering',
              year: 'Sophomore',
              location: 'Berkeley, CA',
              bio: 'Full-stack developer interested in modern web technologies. Always excited to learn new frameworks and best practices.',
              subjects: ['React', 'Node.js', 'JavaScript', 'System Design'],
              skills: {
                'React': 'Advanced',
                'JavaScript': 'Expert',
                'Node.js': 'Intermediate',
                'System Design': 'Beginner'
              },
              studyPreferences: {
                style: 'Project-based learning',
                schedule: 'Weekend',
                duration: '3-4 hours',
                frequency: '1x per week'
              },
              achievements: ['React Certification', 'Open Source Contributor', 'Internship at Google'],
              rating: 4.7,
              completedSessions: 18,
              responseRate: '98%'
            },
            compatibility: 82,
            matchReason: 'Complementary web development skills',
            sharedSubjects: ['JavaScript', 'React', 'System Design'],
            lastActive: '5 minutes ago',
            status: 'online'
          },
          {
            id: 4,
            profile: {
              full_name: 'Michael Torres',
              avatar: '👨‍💼',
              university: 'Harvard',
              major: 'Mathematics',
              year: 'Graduate',
              location: 'Cambridge, MA',
              bio: 'PhD student in Applied Mathematics. Specializing in optimization and numerical methods. Happy to help with calculus and linear algebra.',
              subjects: ['Calculus', 'Linear Algebra', 'Optimization', 'Numerical Methods'],
              skills: {
                'Calculus': 'Expert',
                'Linear Algebra': 'Expert',
                'Optimization': 'Advanced',
                'MATLAB': 'Advanced'
              },
              studyPreferences: {
                style: 'Theoretical approach',
                schedule: 'Morning',
                duration: '2 hours',
                frequency: '2x per week'
              },
              achievements: ['Teaching Assistant', 'Research Grant Recipient', 'Published Papers'],
              rating: 4.9,
              completedSessions: 45,
              responseRate: '90%'
            },
            compatibility: 78,
            matchReason: 'Strong mathematical foundation',
            sharedSubjects: ['Calculus', 'Linear Algebra'],
            lastActive: '30 minutes ago',
            status: 'busy'
          }
        ];
        
        setMatches(mockMatches);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching matches:', error);
      setLoading(false);
    }
  };

  const handleLike = (matchId) => {
    setMatches(matches.map(match => 
      match.id === matchId 
        ? { ...match, liked: !match.liked }
        : match
    ));
  };

  const handleConnect = (matchId) => {
    // Handle connection request
    console.log('Connecting with match:', matchId);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'online': return 'bg-green-400';
      case 'away': return 'bg-yellow-400';
      case 'busy': return 'bg-red-400';
      default: return 'bg-gray-400';
    }
  };

  const getCompatibilityColor = (score) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 80) return 'text-yellow-400';
    if (score >= 70) return 'text-orange-400';
    return 'text-red-400';
  };

  const MatchCard = ({ match }) => (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ y: -5 }}
      className="relative"
    >
      <GlassCard hover className="overflow-hidden">
        {/* Header */}
        <div className="relative p-6 pb-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="text-4xl">{match.profile.avatar}</div>
                <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${getStatusColor(match.status)}`}></div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-black">{match.profile.full_name}</h3>
                <p className="text-gray-600">{match.profile.major} • {match.profile.year}</p>
                <p className="text-gray-500 text-sm flex items-center">
                  <MapPinIcon className="w-4 h-4 mr-1" />
                  {match.profile.university}
                </p>
              </div>
            </div>
            
            {/* Compatibility Score */}
            <div className="text-center">
              <div className={`text-2xl font-bold ${getCompatibilityColor(match.compatibility)}`}>
                {match.compatibility}%
              </div>
              <div className="text-gray-500 text-xs">Match</div>
            </div>
          </div>

          {/* Match Reason */}
          <div className="mt-4 p-3 rounded-lg bg-primary-500/20 border border-primary-400/30">
            <div className="flex items-center text-primary-300 text-sm">
              <SparklesIcon className="w-4 h-4 mr-2" />
              {match.matchReason}
            </div>
          </div>
        </div>

        {/* Bio */}
        <div className="px-6 pb-4">
          <p className="text-gray-700 text-sm leading-relaxed">{match.profile.bio}</p>
        </div>

        {/* Shared Subjects */}
        <div className="px-6 pb-4">
          <h4 className="text-black font-medium mb-2 text-sm">Shared Subjects</h4>
          <div className="flex flex-wrap gap-2">
            {match.sharedSubjects.map((subject, index) => (
              <span
                key={index}
                className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-xs border border-gray-300"
              >
                {subject}
              </span>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="px-6 pb-4">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-black font-semibold">{match.profile.rating}</div>
              <div className="text-gray-500 text-xs flex items-center justify-center">
                <StarIcon className="w-3 h-3 mr-1" />
                Rating
              </div>
            </div>
            <div>
              <div className="text-black font-semibold">{match.profile.completedSessions}</div>
              <div className="text-gray-500 text-xs">Sessions</div>
            </div>
            <div>
              <div className="text-black font-semibold">{match.profile.responseRate}</div>
              <div className="text-gray-500 text-xs">Response</div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="px-6 pb-6 flex space-x-3">
          <GlassButton
            variant="ghost"
            size="sm"
            onClick={() => setSelectedMatch(match)}
            className="flex-1"
          >
            <InformationCircleIcon className="w-4 h-4 mr-2" />
            View Profile
          </GlassButton>
          
          <GlassButton
            variant={match.liked ? "secondary" : "ghost"}
            size="sm"
            onClick={() => handleLike(match.id)}
          >
            {match.liked ? <HeartSolid className="w-4 h-4 text-red-400" /> : <HeartIcon className="w-4 h-4" />}
          </GlassButton>
          
          <GlassButton
            variant="primary"
            size="sm"
            onClick={() => handleConnect(match.id)}
            className="flex-1"
          >
            <UserPlusIcon className="w-4 h-4 mr-2" />
            Connect
          </GlassButton>
        </div>

        {/* Last Active */}
        <div className="px-6 pb-4 border-t border-white/10 pt-4">
          <p className="text-gray-500 text-xs flex items-center">
            <ClockIcon className="w-3 h-3 mr-1" />
            Last active {match.lastActive}
          </p>
        </div>
      </GlassCard>
    </motion.div>
  );

  const DetailModal = ({ match, onClose }) => (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="bg-glass backdrop-blur-xl border border-gray-300 rounded-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="text-6xl">{match.profile.avatar}</div>
                <div className={`absolute -bottom-2 -right-2 w-6 h-6 rounded-full border-2 border-white ${getStatusColor(match.status)}`}></div>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-black">{match.profile.full_name}</h2>
                <p className="text-gray-600">{match.profile.major} • {match.profile.year}</p>
                <p className="text-gray-500 flex items-center">
                  <MapPinIcon className="w-4 h-4 mr-1" />
                  {match.profile.university}, {match.profile.location}
                </p>
              </div>
            </div>
            
            <GlassButton variant="ghost" size="sm" onClick={onClose}>
              <XMarkIcon className="w-5 h-5" />
            </GlassButton>
          </div>

          {/* Bio */}
          <div className="mb-6">
            <h3 className="text-black font-semibold mb-2">About</h3>
            <p className="text-gray-700 leading-relaxed">{match.profile.bio}</p>
          </div>

          {/* Skills */}
          <div className="mb-6">
            <h3 className="text-black font-semibold mb-3">Skills & Expertise</h3>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(match.profile.skills).map(([skill, level]) => (
                <div key={skill} className="flex justify-between items-center p-3 rounded-lg bg-gray-50">
                  <span className="text-gray-700">{skill}</span>
                  <span className={`text-sm font-medium ${
                    level === 'Expert' ? 'text-green-400' :
                    level === 'Advanced' ? 'text-blue-400' :
                    level === 'Intermediate' ? 'text-yellow-400' :
                    'text-orange-400'
                  }`}>
                    {level}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Study Preferences */}
          <div className="mb-6">
            <h3 className="text-black font-semibold mb-3">Study Preferences</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-lg bg-gray-50">
                <div className="text-gray-500 text-sm">Style</div>
                <div className="text-black">{match.profile.studyPreferences.style}</div>
              </div>
              <div className="p-3 rounded-lg bg-gray-50">
                <div className="text-gray-500 text-sm">Schedule</div>
                <div className="text-black">{match.profile.studyPreferences.schedule}</div>
              </div>
              <div className="p-3 rounded-lg bg-gray-50">
                <div className="text-gray-500 text-sm">Duration</div>
                <div className="text-black">{match.profile.studyPreferences.duration}</div>
              </div>
              <div className="p-3 rounded-lg bg-gray-50">
                <div className="text-gray-500 text-sm">Frequency</div>
                <div className="text-black">{match.profile.studyPreferences.frequency}</div>
              </div>
            </div>
          </div>

          {/* Achievements */}
          <div className="mb-6">
            <h3 className="text-black font-semibold mb-3">Achievements</h3>
            <div className="space-y-2">
              {match.profile.achievements.map((achievement, index) => (
                <div key={index} className="flex items-center p-3 rounded-lg bg-gray-50">
                  <AcademicCapIcon className="w-5 h-5 text-yellow-400 mr-3" />
                  <span className="text-gray-700">{achievement}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3">
            <GlassButton
              variant="primary"
              onClick={() => handleConnect(match.id)}
              className="flex-1"
            >
              <UserPlusIcon className="w-5 h-5 mr-2" />
              Send Connection Request
            </GlassButton>
            
            <GlassButton
              variant="secondary"
              className="flex-1"
            >
              <ChatBubbleLeftRightIcon className="w-5 h-5 mr-2" />
              Start Chat
            </GlassButton>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Finding your perfect study matches..." />
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
          Find Your Perfect{' '}
          <span className="text-gradient bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
            Study Partners
          </span>
        </h1>
        <p className="text-xl text-gray-700">
          Connect with like-minded learners who share your academic interests
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <GlassCard>
          <div className="grid md:grid-cols-4 gap-4">
            <div>
              <label className="block text-gray-600 text-sm mb-2">Subject</label>
              <select
                value={filterCriteria.subject}
                onChange={(e) => setFilterCriteria({ ...filterCriteria, subject: e.target.value })}
                className="w-full p-2 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400"
              >
                <option value="">All Subjects</option>
                <option value="machine-learning">Machine Learning</option>
                <option value="web-development">Web Development</option>
                <option value="data-science">Data Science</option>
                <option value="mathematics">Mathematics</option>
              </select>
            </div>
            
            <div>
              <label className="block text-gray-600 text-sm mb-2">Skill Level</label>
              <select
                value={filterCriteria.skillLevel}
                onChange={(e) => setFilterCriteria({ ...filterCriteria, skillLevel: e.target.value })}
                className="w-full p-2 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400"
              >
                <option value="">All Levels</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="expert">Expert</option>
              </select>
            </div>
            
            <div>
              <label className="block text-gray-600 text-sm mb-2">Study Style</label>
              <select
                value={filterCriteria.studyStyle}
                onChange={(e) => setFilterCriteria({ ...filterCriteria, studyStyle: e.target.value })}
                className="w-full p-2 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400"
              >
                <option value="">All Styles</option>
                <option value="visual">Visual Learner</option>
                <option value="hands-on">Hands-on</option>
                <option value="theoretical">Theoretical</option>
                <option value="project-based">Project-based</option>
              </select>
            </div>
            
            <div>
              <label className="block text-gray-600 text-sm mb-2">Availability</label>
              <select
                value={filterCriteria.availability}
                onChange={(e) => setFilterCriteria({ ...filterCriteria, availability: e.target.value })}
                className="w-full p-2 rounded-lg bg-gray-100 border border-gray-300 text-black focus:outline-none focus:border-primary-400"
              >
                <option value="">Any Time</option>
                <option value="morning">Morning</option>
                <option value="afternoon">Afternoon</option>
                <option value="evening">Evening</option>
                <option value="weekend">Weekend</option>
              </select>
            </div>
          </div>
        </GlassCard>
      </motion.div>

      {/* Matches Grid */}
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
          {matches.map((match) => (
            <motion.div
              key={match.id}
              variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            >
              <MatchCard match={match} />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>

      {/* Detail Modal */}
      {selectedMatch && (
        <DetailModal 
          match={selectedMatch} 
          onClose={() => setSelectedMatch(null)} 
        />
      )}
    </div>
  );
};

export default Matches;