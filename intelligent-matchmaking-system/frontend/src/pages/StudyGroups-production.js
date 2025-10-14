import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';

const StudyGroups = () => {
  const { user } = useAuth();
  const [studyGroups, setStudyGroups] = useState([]);
  const [myGroups, setMyGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [activeTab, setActiveTab] = useState('discover');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    topics: [],
    max_members: 10,
    schedule: '',
    location: 'Virtual'
  });

  useEffect(() => {
    fetchStudyGroups();
  }, [activeTab]);

  const fetchStudyGroups = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/matches/study-groups');
      
      if (activeTab === 'discover') {
        setStudyGroups(response.data || []);
      } else if (activeTab === 'my-groups') {
        const myGroupsData = (response.data || []).filter(group => 
          group.members?.some(member => member.user_id === user?.id)
        );
        setMyGroups(myGroupsData);
      }
    } catch (error) {
      console.error('Error fetching study groups:', error);
      toast.error('Failed to load study groups');
      setStudyGroups([]);
      setMyGroups([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/matches/study-groups', formData);
      toast.success('Study group created successfully!');
      setShowCreateModal(false);
      setFormData({
        name: '',
        description: '',
        topics: [],
        max_members: 10,
        schedule: '',
        location: 'Virtual'
      });
      fetchStudyGroups();
    } catch (error) {
      console.error('Error creating study group:', error);
      toast.error('Failed to create study group');
    }
  };

  const handleJoinGroup = async (groupId) => {
    try {
      await axios.post(`/matches/study-groups/${groupId}/join`, {
        introduction: 'Hello! I would like to join this group.'
      });
      toast.success('Successfully joined the group!');
      fetchStudyGroups();
    } catch (error) {
      console.error('Error joining group:', error);
      toast.error(error.response?.data?.detail || 'Failed to join group');
    }
  };

  const filteredGroups = (activeTab === 'discover' ? studyGroups : myGroups).filter(group =>
    group.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    group.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    group.topics?.some(topic => topic.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Study Groups</h1>
            <p className="text-gray-600 dark:text-gray-400">
              Join or create study groups to learn together
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2"
          >
            <span className="material-symbols-outlined">add</span>
            Create Group
          </button>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-6 border-b border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setActiveTab('discover')}
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              activeTab === 'discover'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-600 dark:text-gray-400'
            }`}
          >
            Discover Groups
          </button>
          <button
            onClick={() => setActiveTab('my-groups')}
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              activeTab === 'my-groups'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-600 dark:text-gray-400'
            }`}
          >
            My Groups
          </button>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search groups..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Groups List */}
        {loading ? (
          <div className="flex justify-center py-12">
            <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
          </div>
        ) : filteredGroups.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredGroups.map((group) => (
              <motion.div
                key={group.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              >
                <h3 className="text-xl font-bold mb-2">{group.name}</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
                  {group.description}
                </p>
                
                {/* Topics */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {group.topics?.slice(0, 3).map((topic, i) => (
                    <span key={i} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">
                      {topic}
                    </span>
                  ))}
                </div>

                {/* Members */}
                <div className="flex items-center gap-2 mb-4 text-sm text-gray-600 dark:text-gray-400">
                  <span className="material-symbols-outlined text-lg">group</span>
                  <span>{group.members?.length || 0} / {group.max_members} members</span>
                </div>

                {/* Action Button */}
                <button
                  onClick={() => handleJoinGroup(group.id)}
                  disabled={group.members?.some(m => m.user_id === user?.id)}
                  className={`w-full py-2 rounded-lg font-medium transition-colors ${
                    group.members?.some(m => m.user_id === user?.id)
                      ? 'bg-gray-300 dark:bg-gray-700 cursor-not-allowed'
                      : 'bg-primary text-white hover:bg-primary/90'
                  }`}
                >
                  {group.members?.some(m => m.user_id === user?.id) ? 'Joined' : 'Join Group'}
                </button>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <span className="material-symbols-outlined text-6xl text-gray-400 mb-4">groups</span>
            <h3 className="text-xl font-semibold mb-2">No groups found</h3>
            <p className="text-gray-600 dark:text-gray-400">
              {activeTab === 'my-groups' ? 'Join a group to get started!' : 'Be the first to create a group!'}
            </p>
          </div>
        )}

        {/* Create Group Modal */}
        <AnimatePresence>
          {showCreateModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
              onClick={() => setShowCreateModal(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full"
                onClick={(e) => e.stopPropagation()}
              >
                <h2 className="text-2xl font-bold mb-4">Create Study Group</h2>
                <form onSubmit={handleCreateGroup}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Group Name</label>
                      <input
                        type="text"
                        required
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                        placeholder="e.g., Machine Learning Study Group"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Description</label>
                      <textarea
                        required
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 resize-none"
                        rows="3"
                        placeholder="What will this group focus on?"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Max Members</label>
                      <input
                        type="number"
                        required
                        min="2"
                        max="50"
                        value={formData.max_members}
                        onChange={(e) => setFormData({ ...formData, max_members: parseInt(e.target.value) })}
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                      />
                    </div>
                    <div className="flex gap-3">
                      <button
                        type="button"
                        onClick={() => setShowCreateModal(false)}
                        className="flex-1 py-2 rounded-lg border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        className="flex-1 py-2 rounded-lg bg-primary text-white hover:bg-primary/90"
                      >
                        Create
                      </button>
                    </div>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default StudyGroups;
