import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpenIcon,
  VideoCameraIcon,
  DocumentTextIcon,
  LinkIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  StarIcon,
  ClockIcon,
  EyeIcon,
  BookmarkIcon,
  PlayIcon,
  DownloadIcon,
  ShareIcon,
  HeartIcon,
  AcademicCapIcon,
  LightBulbIcon,
  CodeBracketIcon,
  CalculatorIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarSolid, BookmarkIcon as BookmarkSolid, HeartIcon as HeartSolid } from '@heroicons/react/24/solid';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';
import GlassButton from '../components/ui/GlassButton';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const Resources = () => {
  const { user } = useAuth();
  const [resources, setResources] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedResource, setSelectedResource] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [sortBy, setSortBy] = useState('popular'); // popular, recent, rating
  const [filterType, setFilterType] = useState(''); // video, article, course, tool
  const [loading, setLoading] = useState(true);
  const [bookmarkedResources, setBookmarkedResources] = useState(new Set());
  const [likedResources, setLikedResources] = useState(new Set());

  useEffect(() => {
    fetchResources();
    fetchCategories();
  }, [searchQuery, selectedCategory, sortBy, filterType]);

  const fetchCategories = async () => {
    const mockCategories = [
      { id: 'machine-learning', name: 'Machine Learning', icon: '🤖', count: 234 },
      { id: 'web-development', name: 'Web Development', icon: '💻', count: 189 },
      { id: 'data-science', name: 'Data Science', icon: '📊', count: 156 },
      { id: 'programming', name: 'Programming', icon: '⚡', count: 298 },
      { id: 'mathematics', name: 'Mathematics', icon: '📐', count: 145 },
      { id: 'algorithms', name: 'Algorithms', icon: '🔍', count: 123 },
      { id: 'design', name: 'Design', icon: '🎨', count: 87 },
      { id: 'mobile-dev', name: 'Mobile Development', icon: '📱', count: 92 }
    ];
    setCategories(mockCategories);
  };

  const fetchResources = async () => {
    try {
      setLoading(true);
      
      // Simulate API call with mock data
      setTimeout(() => {
        const mockResources = [
          {
            id: 1,
            title: 'Complete Machine Learning Course 2024',
            description: 'Comprehensive course covering supervised and unsupervised learning, neural networks, and practical applications with Python.',
            type: 'course',
            category: 'machine-learning',
            author: {
              name: 'Dr. Sarah Chen',
              avatar: '👩‍🏫',
              credentials: 'PhD, Stanford University'
            },
            thumbnail: 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=400',
            duration: '12 hours',
            level: 'Beginner to Advanced',
            rating: 4.9,
            reviews: 2847,
            views: 45672,
            likes: 3421,
            bookmarks: 1654,
            tags: ['Python', 'TensorFlow', 'Scikit-learn', 'Deep Learning'],
            createdAt: '2024-01-15',
            updatedAt: '2024-01-20',
            url: 'https://example.com/ml-course',
            isPublic: true,
            isFeatured: true,
            content: {
              chapters: [
                'Introduction to Machine Learning',
                'Supervised Learning',
                'Unsupervised Learning',
                'Neural Networks',
                'Deep Learning',
                'Real-world Projects'
              ],
              totalLessons: 78,
              totalQuizzes: 12,
              totalProjects: 6
            }
          },
          {
            id: 2,
            title: 'React Hooks Explained: Complete Guide',
            description: 'Deep dive into React Hooks with practical examples and best practices. Learn useState, useEffect, useContext, and custom hooks.',
            type: 'article',
            category: 'web-development',
            author: {
              name: 'Alex Rodriguez',
              avatar: '👨‍💻',
              credentials: 'Senior Frontend Developer, Meta'
            },
            thumbnail: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400',
            duration: '15 min read',
            level: 'Intermediate',
            rating: 4.8,
            reviews: 1234,
            views: 23456,
            likes: 1876,
            bookmarks: 932,
            tags: ['React', 'JavaScript', 'Frontend', 'Hooks'],
            createdAt: '2024-01-18',
            updatedAt: '2024-01-22',
            url: 'https://example.com/react-hooks',
            isPublic: true,
            isFeatured: false,
            content: {
              sections: [
                'Introduction to Hooks',
                'useState Hook',
                'useEffect Hook',
                'useContext Hook',
                'Custom Hooks',
                'Best Practices'
              ],
              codeExamples: 15,
              interactiveDemo: true
            }
          },
          {
            id: 3,
            title: 'Data Visualization with Python',
            description: 'Master data visualization using Matplotlib, Seaborn, and Plotly. Create stunning charts and interactive dashboards.',
            type: 'video',
            category: 'data-science',
            author: {
              name: 'Emily Zhang',
              avatar: '👩‍🔬',
              credentials: 'Data Scientist, Google'
            },
            thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400',
            duration: '2.5 hours',
            level: 'Intermediate',
            rating: 4.7,
            reviews: 892,
            views: 18943,
            likes: 1432,
            bookmarks: 678,
            tags: ['Python', 'Matplotlib', 'Seaborn', 'Plotly', 'Data Viz'],
            createdAt: '2024-01-12',
            updatedAt: '2024-01-16',
            url: 'https://example.com/data-viz-python',
            isPublic: true,
            isFeatured: true,
            content: {
              chapters: [
                'Introduction to Data Visualization',
                'Matplotlib Basics',
                'Advanced Matplotlib',
                'Seaborn for Statistical Plots',
                'Interactive Plots with Plotly',
                'Dashboard Creation'
              ],
              exercises: 12,
              datasets: 5
            }
          },
          {
            id: 4,
            title: 'Algorithm Design Patterns',
            description: 'Essential algorithm design patterns every programmer should know. Includes dynamic programming, greedy algorithms, and divide & conquer.',
            type: 'document',
            category: 'algorithms',
            author: {
              name: 'Prof. Michael Torres',
              avatar: '👨‍🎓',
              credentials: 'Professor of Computer Science, MIT'
            },
            thumbnail: 'https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=400',
            duration: '45 min read',
            level: 'Advanced',
            rating: 4.9,
            reviews: 567,
            views: 12345,
            likes: 987,
            bookmarks: 543,
            tags: ['Algorithms', 'Design Patterns', 'Programming', 'Computer Science'],
            createdAt: '2024-01-10',
            updatedAt: '2024-01-14',
            url: 'https://example.com/algorithm-patterns',
            isPublic: true,
            isFeatured: false,
            content: {
              sections: [
                'Introduction to Design Patterns',
                'Dynamic Programming',
                'Greedy Algorithms',
                'Divide and Conquer',
                'Backtracking',
                'Practice Problems'
              ],
              examples: 25,
              exercises: 18
            }
          },
          {
            id: 5,
            title: 'CSS Grid Layout Mastery',
            description: 'Complete guide to CSS Grid Layout. Build complex responsive layouts with ease using modern CSS Grid techniques.',
            type: 'video',
            category: 'web-development',
            author: {
              name: 'Jordan Smith',
              avatar: '👨‍🎨',
              credentials: 'UI/UX Designer & Frontend Developer'
            },
            thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
            duration: '3 hours',
            level: 'Beginner to Intermediate',
            rating: 4.6,
            reviews: 743,
            views: 15678,
            likes: 1123,
            bookmarks: 567,
            tags: ['CSS', 'Grid Layout', 'Responsive Design', 'Frontend'],
            createdAt: '2024-01-08',
            updatedAt: '2024-01-12',
            url: 'https://example.com/css-grid',
            isPublic: true,
            isFeatured: false,
            content: {
              lessons: [
                'Grid Basics',
                'Grid Container Properties',
                'Grid Item Properties',
                'Responsive Grids',
                'Real-world Examples',
                'Grid vs Flexbox'
              ],
              codepen: 12,
              challenges: 8
            }
          },
          {
            id: 6,
            title: 'Statistics for Data Science',
            description: 'Fundamental statistics concepts for data scientists. Covers descriptive statistics, probability, hypothesis testing, and more.',
            type: 'course',
            category: 'mathematics',
            author: {
              name: 'Dr. Lisa Wang',
              avatar: '👩‍🔬',
              credentials: 'PhD Statistics, Harvard University'
            },
            thumbnail: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400',
            duration: '8 hours',
            level: 'Beginner',
            rating: 4.8,
            reviews: 1456,
            views: 28934,
            likes: 2156,
            bookmarks: 1234,
            tags: ['Statistics', 'Probability', 'Data Science', 'Mathematics'],
            createdAt: '2024-01-05',
            updatedAt: '2024-01-18',
            url: 'https://example.com/statistics-ds',
            isPublic: true,
            isFeatured: true,
            content: {
              modules: [
                'Descriptive Statistics',
                'Probability Theory',
                'Distributions',
                'Hypothesis Testing',
                'Regression Analysis',
                'Bayesian Statistics'
              ],
              quizzes: 15,
              assignments: 6
            }
          }
        ];
        
        // Filter and sort resources based on current filters
        let filteredResources = mockResources;
        
        if (searchQuery) {
          filteredResources = filteredResources.filter(resource =>
            resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            resource.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            resource.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
          );
        }
        
        if (selectedCategory) {
          filteredResources = filteredResources.filter(resource =>
            resource.category === selectedCategory
          );
        }
        
        if (filterType) {
          filteredResources = filteredResources.filter(resource =>
            resource.type === filterType
          );
        }
        
        // Sort resources
        switch (sortBy) {
          case 'recent':
            filteredResources.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            break;
          case 'rating':
            filteredResources.sort((a, b) => b.rating - a.rating);
            break;
          case 'popular':
          default:
            filteredResources.sort((a, b) => b.views - a.views);
            break;
        }
        
        setResources(filteredResources);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching resources:', error);
      setLoading(false);
    }
  };

  const handleBookmark = (resourceId) => {
    setBookmarkedResources(prev => {
      const newSet = new Set(prev);
      if (newSet.has(resourceId)) {
        newSet.delete(resourceId);
      } else {
        newSet.add(resourceId);
      }
      return newSet;
    });
  };

  const handleLike = (resourceId) => {
    setLikedResources(prev => {
      const newSet = new Set(prev);
      if (newSet.has(resourceId)) {
        newSet.delete(resourceId);
      } else {
        newSet.add(resourceId);
      }
      return newSet;
    });
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'video': return VideoCameraIcon;
      case 'article': return DocumentTextIcon;
      case 'course': return AcademicCapIcon;
      case 'document': return BookOpenIcon;
      case 'tool': return CodeBracketIcon;
      default: return BookOpenIcon;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'video': return 'text-red-400 bg-red-400/20';
      case 'article': return 'text-blue-400 bg-blue-400/20';
      case 'course': return 'text-green-400 bg-green-400/20';
      case 'document': return 'text-purple-400 bg-purple-400/20';
      case 'tool': return 'text-yellow-400 bg-yellow-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getLevelColor = (level) => {
    if (level.includes('Beginner')) return 'text-green-400';
    if (level.includes('Intermediate')) return 'text-yellow-400';
    if (level.includes('Advanced')) return 'text-red-400';
    return 'text-blue-400';
  };

  const ResourceCard = ({ resource }) => {
    const TypeIcon = getTypeIcon(resource.type);
    const isBookmarked = bookmarkedResources.has(resource.id);
    const isLiked = likedResources.has(resource.id);

    return (
      <motion.div
        layout
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        whileHover={{ y: -5 }}
      >
        <GlassCard hover className="h-full overflow-hidden group">
          {/* Thumbnail */}
          <div className="relative h-48 overflow-hidden">
            <div className="w-full h-full bg-gradient-to-br from-primary-500/20 to-secondary-500/20 flex items-center justify-center">
              <TypeIcon className="w-16 h-16 text-black/30" />
            </div>
            
            {/* Overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
            
            {/* Type Badge */}
            <div className={`absolute top-3 left-3 px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(resource.type)}`}>
              {resource.type.charAt(0).toUpperCase() + resource.type.slice(1)}
            </div>
            
            {/* Featured Badge */}
            {resource.isFeatured && (
              <div className="absolute top-3 right-3 px-2 py-1 rounded-full bg-yellow-400/20 text-yellow-400 text-xs font-medium">
                Featured
              </div>
            )}
            
            {/* Duration */}
            <div className="absolute bottom-3 right-3 px-2 py-1 rounded bg-black/60 text-black text-xs">
              {resource.duration}
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {/* Title */}
            <h3 className="text-lg font-bold text-black mb-2 line-clamp-2 group-hover:text-primary-300 transition-colors">
              {resource.title}
            </h3>
            
            {/* Description */}
            <p className="text-gray-600 text-sm mb-4 line-clamp-3">
              {resource.description}
            </p>
            
            {/* Author */}
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">{resource.author.avatar}</span>
              <div>
                <div className="text-gray-700 text-sm font-medium">{resource.author.name}</div>
                <div className="text-gray-500 text-xs">{resource.author.credentials}</div>
              </div>
            </div>
            
            {/* Tags */}
            <div className="flex flex-wrap gap-1 mb-4">
              {resource.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 rounded-full bg-gray-100 text-gray-600 text-xs"
                >
                  {tag}
                </span>
              ))}
              {resource.tags.length > 3 && (
                <span className="px-2 py-1 rounded-full bg-gray-100 text-gray-500 text-xs">
                  +{resource.tags.length - 3}
                </span>
              )}
            </div>
            
            {/* Stats */}
            <div className="flex items-center justify-between text-xs text-black/60 mb-4">
              <div className="flex items-center space-x-4">
                <span className="flex items-center">
                  <StarIcon className="w-3 h-3 mr-1" />
                  {resource.rating}
                </span>
                <span className="flex items-center">
                  <EyeIcon className="w-3 h-3 mr-1" />
                  {resource.views.toLocaleString()}
                </span>
                <span className={`font-medium ${getLevelColor(resource.level)}`}>
                  {resource.level}
                </span>
              </div>
            </div>
            
            {/* Actions */}
            <div className="flex items-center justify-between">
              <GlassButton
                variant="primary"
                size="sm"
                onClick={() => setSelectedResource(resource)}
              >
                <PlayIcon className="w-4 h-4 mr-2" />
                View
              </GlassButton>
              
              <div className="flex space-x-2">
                <GlassButton
                  variant="ghost"
                  size="sm"
                  onClick={() => handleLike(resource.id)}
                >
                  {isLiked ? (
                    <HeartSolid className="w-4 h-4 text-red-400" />
                  ) : (
                    <HeartIcon className="w-4 h-4" />
                  )}
                </GlassButton>
                
                <GlassButton
                  variant="ghost"
                  size="sm"
                  onClick={() => handleBookmark(resource.id)}
                >
                  {isBookmarked ? (
                    <BookmarkSolid className="w-4 h-4 text-blue-400" />
                  ) : (
                    <BookmarkIcon className="w-4 h-4" />
                  )}
                </GlassButton>
                
                <GlassButton
                  variant="ghost"
                  size="sm"
                >
                  <ShareIcon className="w-4 h-4" />
                </GlassButton>
              </div>
            </div>
          </div>
        </GlassCard>
      </motion.div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading learning resources..." />
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
          Learning{' '}
          <span className="text-gradient bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
            Resources
          </span>
        </h1>
        <p className="text-xl text-gray-700">
          Curated collection of high-quality educational content
        </p>
      </motion.div>

      {/* Categories */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="flex overflow-x-auto space-x-4 pb-4">
          <button
            onClick={() => setSelectedCategory('')}
            className={`flex-shrink-0 px-4 py-2 rounded-lg transition-all ${
              selectedCategory === ''
                ? 'bg-primary-500 text-black shadow-lg'
                : 'bg-gray-100 text-gray-600 hover:bg-white/20'
            }`}
          >
            All Categories
          </button>
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex-shrink-0 flex items-center px-4 py-2 rounded-lg transition-all ${
                selectedCategory === category.id
                  ? 'bg-primary-500 text-black shadow-lg'
                  : 'bg-gray-100 text-gray-600 hover:bg-white/20'
              }`}
            >
              <span className="mr-2">{category.icon}</span>
              {category.name}
              <span className="ml-2 px-2 py-0.5 rounded-full bg-white/20 text-xs">
                {category.count}
              </span>
            </button>
          ))}
        </div>
      </motion.div>

      {/* Search and Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <GlassCard>
          <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
            {/* Search */}
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search resources..."
                className="w-full pl-10 pr-4 py-3 rounded-lg bg-gray-100 border border-gray-300 text-black placeholder-white/50 focus:outline-none focus:border-primary-400"
              />
            </div>
            
            {/* Filters */}
            <div className="flex flex-wrap gap-3">
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-2 rounded-lg bg-gray-100 border border-gray-300 text-black text-sm focus:outline-none focus:border-primary-400"
              >
                <option value="">All Types</option>
                <option value="video">Videos</option>
                <option value="article">Articles</option>
                <option value="course">Courses</option>
                <option value="document">Documents</option>
              </select>
              
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2 rounded-lg bg-gray-100 border border-gray-300 text-black text-sm focus:outline-none focus:border-primary-400"
              >
                <option value="popular">Most Popular</option>
                <option value="recent">Most Recent</option>
                <option value="rating">Highest Rated</option>
              </select>
            </div>
          </div>
        </GlassCard>
      </motion.div>

      {/* Resources Grid */}
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
          {resources.map((resource) => (
            <motion.div
              key={resource.id}
              variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            >
              <ResourceCard resource={resource} />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>

      {/* Empty State */}
      {resources.length === 0 && (
        <motion.div
          className="text-center py-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="text-6xl mb-4">📚</div>
          <h3 className="text-xl font-semibold text-black mb-2">No resources found</h3>
          <p className="text-gray-600 mb-6">
            Try adjusting your search terms or filters
          </p>
          <GlassButton
            variant="primary"
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('');
              setFilterType('');
            }}
          >
            Clear Filters
          </GlassButton>
        </motion.div>
      )}
    </div>
  );
};

export default Resources;