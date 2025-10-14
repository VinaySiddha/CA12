import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';

const Resources = () => {
  const { user } = useAuth();
  const [resources, setResources] = useState([]);
  const [categories, setCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');

  useEffect(() => {
    fetchResources();
    fetchCategories();
  }, [activeCategory, selectedDifficulty]);

  const fetchResources = async () => {
    setLoading(true);
    try {
      let url = '/resources/';
      const params = {};
      
      if (activeCategory !== 'all') {
        params.category = activeCategory;
      }
      
      if (selectedDifficulty !== 'all') {
        params.difficulty = selectedDifficulty;
      }
      
      const response = await axios.get(url, { params });
      setResources(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
      toast.error('Failed to load resources');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('/resources/categories');
      setCategories(['all', ...response.data.categories]);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchResources();
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get('/resources/', {
        params: { search: searchQuery }
      });
      setResources(response.data);
    } catch (error) {
      console.error('Error searching resources:', error);
      toast.error('Search failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (resourceId) => {
    try {
      await axios.post(`/resources/${resourceId}/like`);
      fetchResources(); // Refresh to show updated likes
      toast.success('Resource liked!');
    } catch (error) {
      console.error('Error liking resource:', error);
      toast.error('Failed to like resource');
    }
  };

  const handleDownload = async (resourceId, fileName) => {
    try {
      const response = await axios.get(`/resources/${resourceId}/download`, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName || 'download');
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Download started!');
    } catch (error) {
      console.error('Error downloading resource:', error);
      toast.error('Failed to download resource');
    }
  };

  const getResourceTypeInfo = (type) => {
    const types = {
      pdf: { icon: 'picture_as_pdf', color: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400' },
      video: { icon: 'play_circle', color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' },
      article: { icon: 'article', color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400' },
      code: { icon: 'code', color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400' },
      document: { icon: 'description', color: 'bg-gray-100 text-gray-600 dark:bg-gray-900/30 dark:text-gray-400' }
    };
    return types[type] || types.document;
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      beginner: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
      intermediate: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
      advanced: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
    };
    return colors[difficulty] || colors.intermediate;
  };

  if (loading && resources.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Learning Resources</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Browse educational materials uploaded by experts and teachers
        </p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 mb-6 shadow-sm">
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search resources..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="w-full px-4 py-3 pl-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-primary focus:border-transparent"
            />
            <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
              search
            </span>
          </div>
          <button
            onClick={handleSearch}
            className="bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-lg font-semibold"
          >
            Search
          </button>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-4">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                activeCategory === category
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {category === 'all' ? 'All' : category}
            </button>
          ))}
        </div>

        {/* Difficulty Filter */}
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-gray-600 dark:text-gray-400 self-center mr-2">Difficulty:</span>
          {['all', 'beginner', 'intermediate', 'advanced'].map((level) => (
            <button
              key={level}
              onClick={() => setSelectedDifficulty(level)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                selectedDifficulty === level
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Upload Button for Teachers/Admins */}
      {(user?.role === 'teacher' || user?.role === 'expert' || user?.role === 'admin') && (
        <div className="mb-6">
          <a
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-primary hover:bg-primary/90 text-white py-3 px-6 rounded-lg font-semibold"
          >
            <span className="material-symbols-outlined">add</span>
            Upload Resource (Go to Dashboard)
          </a>
        </div>
      )}

      {/* Resources Grid */}
      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        </div>
      ) : resources.length === 0 ? (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
          <span className="material-symbols-outlined text-6xl text-gray-400 mb-4">folder_open</span>
          <p className="text-gray-600 dark:text-gray-400">No resources found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {resources.map((resource) => {
            const typeInfo = getResourceTypeInfo(resource.resource_type);
            const isLiked = resource.likes?.includes(user?._id);
            
            return (
              <motion.div
                key={resource._id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                {/* Resource Type Badge */}
                <div className="flex items-start justify-between mb-3">
                  <div className={`${typeInfo.color} px-3 py-1 rounded-lg flex items-center gap-2`}>
                    <span className="material-symbols-outlined text-lg">{typeInfo.icon}</span>
                    <span className="text-sm font-medium">{resource.resource_type.toUpperCase()}</span>
                  </div>
                  <span className={`${getDifficultyColor(resource.difficulty_level)} px-3 py-1 rounded-full text-xs font-medium`}>
                    {resource.difficulty_level}
                  </span>
                </div>

                {/* Title and Description */}
                <h3 className="text-xl font-semibold mb-2">{resource.title}</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
                  {resource.description}
                </p>

                {/* Category and Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-full text-xs">
                    {resource.category}
                  </span>
                  {resource.tags?.slice(0, 3).map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                {/* Author and Stats */}
                <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-lg">person</span>
                    <span>{resource.uploader_name}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span>👁 {resource.views || 0}</span>
                    <span>⬇️ {resource.downloads || 0}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  {resource.file_id ? (
                    <button
                      onClick={() => handleDownload(resource._id, resource.file_name)}
                      className="flex-1 bg-primary hover:bg-primary/90 text-white py-2 px-4 rounded-lg font-semibold flex items-center justify-center gap-2"
                    >
                      <span className="material-symbols-outlined">download</span>
                      Download
                    </button>
                  ) : resource.external_url ? (
                    <a
                      href={resource.external_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 bg-primary hover:bg-primary/90 text-white py-2 px-4 rounded-lg font-semibold flex items-center justify-center gap-2"
                    >
                      <span className="material-symbols-outlined">open_in_new</span>
                      Open Link
                    </a>
                  ) : null}
                  
                  <button
                    onClick={() => handleLike(resource._id)}
                    className={`px-4 py-2 rounded-lg font-semibold flex items-center gap-2 ${
                      isLiked
                        ? 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }`}
                  >
                    <span className="material-symbols-outlined">{isLiked ? 'favorite' : 'favorite_border'}</span>
                    {resource.likes?.length || 0}
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Resources;
