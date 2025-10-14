import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

const Matches = () => {
  const { user } = useAuth();
  const [matches, setMatches] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('expert-matches'); // expert-matches, connections

  useEffect(() => {
    fetchMatches();
  }, [activeTab]);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      
      if (activeTab === 'expert-matches' && user?.role === 'student') {
        // Fetch expert matches for students
        const response = await axios.get('/matches/expert-matches?limit=10');
        setMatches(response.data || []);
      } else {
        // Fetch general ML recommendations
        const response = await axios.get('/matches/ml-recommendations?limit=10');
        setMatches(response.data || []);
      }
    } catch (error) {
      console.error('Error fetching matches:', error);
      toast.error('Failed to load matches');
      setMatches([]);
    } finally {
      setLoading(false);
    }
  };

  const handleConnect = async (matchId) => {
    try {
      // Implement connection logic
      toast.success('Connection request sent!');
    } catch (error) {
      console.error('Error connecting:', error);
      toast.error('Failed to send connection request');
    }
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Matches</h1>
          <p className="text-gray-600 dark:text-gray-400">
            AI-powered matches based on your interests and learning goals
          </p>
        </div>

        {/* Tabs */}
        {user?.role === 'student' && (
          <div className="flex gap-4 mb-6 border-b border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setActiveTab('expert-matches')}
              className={`px-6 py-3 font-medium border-b-2 transition-colors ${
                activeTab === 'expert-matches'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-600 dark:text-gray-400'
              }`}
            >
              Expert Matches
            </button>
            <button
              onClick={() => setActiveTab('connections')}
              className={`px-6 py-3 font-medium border-b-2 transition-colors ${
                activeTab === 'connections'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-600 dark:text-gray-400'
              }`}
            >
              Peer Matches
            </button>
          </div>
        )}

        {/* Matches Grid */}
        {loading ? (
          <div className="flex justify-center py-12">
            <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
          </div>
        ) : matches.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {matches.map((match, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              >
                {/* Avatar */}
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white font-bold text-2xl">
                    {match.full_name?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-lg">{match.full_name || 'User'}</h3>
                    {match.job_title && <p className="text-sm text-gray-600 dark:text-gray-400">{match.job_title}</p>}
                    {match.company && <p className="text-xs text-gray-500">@ {match.company}</p>}
                  </div>
                </div>

                {/* Match Score */}
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Match Score</span>
                    <span className="font-bold text-primary">{((match.match_score || match.similarity_score || 0) * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-primary to-purple-600 h-2 rounded-full transition-all"
                      style={{ width: `${((match.match_score || match.similarity_score || 0) * 100)}%` }}
                    />
                  </div>
                </div>

                {/* Expertise/Interests */}
                {match.expertise_areas && match.expertise_areas.length > 0 && (
                  <div className="mb-4">
                    <p className="text-sm font-medium mb-2">Expertise</p>
                    <div className="flex flex-wrap gap-2">
                      {match.expertise_areas.slice(0, 3).map((area, i) => (
                        <span key={i} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Matched Interests */}
                {match.matched_interests && match.matched_interests.length > 0 && (
                  <div className="flex items-center gap-2 mb-4 text-sm text-green-600 dark:text-green-400">
                    <span className="material-symbols-outlined text-sm">check_circle</span>
                    <span>{match.matched_interests.length} shared interests</span>
                  </div>
                )}

                {/* Action Button */}
                <button
                  onClick={() => handleConnect(match.id || match.expert_id)}
                  className="w-full py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors font-medium"
                >
                  Connect
                </button>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <span className="material-symbols-outlined text-6xl text-gray-400 mb-4">people</span>
            <h3 className="text-xl font-semibold mb-2">No matches found</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Complete your profile to get better matches!
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Matches;
