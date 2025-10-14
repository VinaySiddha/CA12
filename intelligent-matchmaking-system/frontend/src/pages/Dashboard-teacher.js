import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';

const TeacherDashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('meetings');
  const [pendingMeetings, setPendingMeetings] = useState([]);
  const [myResources, setMyResources] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Resource upload form state
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [resourceForm, setResourceForm] = useState({
    title: '',
    description: '',
    category: '',
    resource_type: 'pdf',
    tags: '',
    difficulty_level: 'intermediate',
    external_url: '',
    file: null
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [meetingsRes, resourcesRes] = await Promise.all([
        axios.get('/meetings/pending'),
        axios.get('/resources/my-resources')
      ]);
      
      setPendingMeetings(meetingsRes.data);
      setMyResources(resourcesRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleApproveMeeting = async (meetingId) => {
    const googleMeetLink = prompt('Enter Google Meet link:');
    if (!googleMeetLink) return;

    const scheduledDate = prompt('Enter scheduled date/time (YYYY-MM-DD HH:MM):');
    if (!scheduledDate) return;

    try {
      const formattedDate = new Date(scheduledDate).toISOString();
      
      await axios.post(`/meetings/${meetingId}/approve`, {
        scheduled_date: formattedDate,
        google_meet_link: googleMeetLink,
        teacher_notes: 'Looking forward to our meeting!'
      });

      toast.success('Meeting approved successfully!');
      fetchDashboardData();
    } catch (error) {
      console.error('Error approving meeting:', error);
      toast.error(error.response?.data?.detail || 'Failed to approve meeting');
    }
  };

  const handleRejectMeeting = async (meetingId) => {
    const reason = prompt('Enter reason for rejection:');
    if (!reason) return;

    try {
      await axios.post(`/meetings/${meetingId}/reject`, {
        teacher_notes: reason
      });

      toast.success('Meeting rejected');
      fetchDashboardData();
    } catch (error) {
      console.error('Error rejecting meeting:', error);
      toast.error('Failed to reject meeting');
    }
  };

  const handleResourceFormChange = (e) => {
    const { name, value } = e.target;
    setResourceForm(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    setResourceForm(prev => ({ ...prev, file: e.target.files[0] }));
  };

  const handleUploadResource = async (e) => {
    e.preventDefault();
    
    if (!resourceForm.file && !resourceForm.external_url) {
      toast.error('Please provide either a file or external URL');
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('title', resourceForm.title);
      formData.append('description', resourceForm.description);
      formData.append('category', resourceForm.category);
      formData.append('resource_type', resourceForm.resource_type);
      formData.append('tags', resourceForm.tags);
      formData.append('difficulty_level', resourceForm.difficulty_level);
      
      if (resourceForm.file) {
        formData.append('file', resourceForm.file);
      } else {
        formData.append('external_url', resourceForm.external_url);
      }

      await axios.post('/resources/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      toast.success('Resource uploaded successfully!');
      setShowUploadForm(false);
      setResourceForm({
        title: '',
        description: '',
        category: '',
        resource_type: 'pdf',
        tags: '',
        difficulty_level: 'intermediate',
        external_url: '',
        file: null
      });
      fetchDashboardData();
    } catch (error) {
      console.error('Error uploading resource:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload resource');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteResource = async (resourceId) => {
    if (!window.confirm('Are you sure you want to delete this resource?')) return;

    try {
      await axios.delete(`/resources/${resourceId}`);
      toast.success('Resource deleted successfully');
      fetchDashboardData();
    } catch (error) {
      console.error('Error deleting resource:', error);
      toast.error('Failed to delete resource');
    }
  };

  if (loading) {
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
        <h1 className="text-3xl font-bold mb-2">Teacher Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Manage meetings, upload resources, and help students succeed
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">Pending Meetings</p>
              <p className="text-3xl font-bold text-primary">{pendingMeetings.length}</p>
            </div>
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <span className="material-symbols-outlined text-blue-600 dark:text-blue-300">event</span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">My Resources</p>
              <p className="text-3xl font-bold text-green-600">{myResources.length}</p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
              <span className="material-symbols-outlined text-green-600 dark:text-green-300">folder</span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">Total Views</p>
              <p className="text-3xl font-bold text-purple-600">
                {myResources.reduce((sum, r) => sum + (r.views || 0), 0)}
              </p>
            </div>
            <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <span className="material-symbols-outlined text-purple-600 dark:text-purple-300">visibility</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={() => setActiveTab('meetings')}
          className={`pb-4 px-4 font-semibold transition-colors relative ${
            activeTab === 'meetings'
              ? 'text-primary'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
          }`}
        >
          Meeting Requests
          {activeTab === 'meetings' && (
            <motion.div
              layoutId="activeTab"
              className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
            />
          )}
        </button>
        <button
          onClick={() => setActiveTab('resources')}
          className={`pb-4 px-4 font-semibold transition-colors relative ${
            activeTab === 'resources'
              ? 'text-primary'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
          }`}
        >
          My Resources
          {activeTab === 'resources' && (
            <motion.div
              layoutId="activeTab"
              className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
            />
          )}
        </button>
      </div>

      {/* Content */}
      {activeTab === 'meetings' && (
        <div className="space-y-4">
          {pendingMeetings.length === 0 ? (
            <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
              <span className="material-symbols-outlined text-6xl text-gray-400 mb-4">event_available</span>
              <p className="text-gray-600 dark:text-gray-400">No pending meeting requests</p>
            </div>
          ) : (
            pendingMeetings.map((meeting) => (
              <motion.div
                key={meeting._id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold mb-2">{meeting.title}</h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">{meeting.description}</p>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500 dark:text-gray-500">Student:</span>
                        <p className="font-medium">{meeting.student_name}</p>
                      </div>
                      <div>
                        <span className="text-gray-500 dark:text-gray-500">Topic:</span>
                        <p className="font-medium">{meeting.topic}</p>
                      </div>
                      <div>
                        <span className="text-gray-500 dark:text-gray-500">Duration:</span>
                        <p className="font-medium">{meeting.duration_minutes} minutes</p>
                      </div>
                      <div>
                        <span className="text-gray-500 dark:text-gray-500">Preferred Time:</span>
                        <p className="font-medium">
                          {meeting.preferred_date 
                            ? new Date(meeting.preferred_date).toLocaleString()
                            : 'Flexible'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex gap-3 mt-6">
                  <button
                    onClick={() => handleApproveMeeting(meeting._id)}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-semibold transition-colors"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleRejectMeeting(meeting._id)}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-semibold transition-colors"
                  >
                    Reject
                  </button>
                </div>
              </motion.div>
            ))
          )}
        </div>
      )}

      {activeTab === 'resources' && (
        <div>
          {/* Upload Button */}
          <div className="mb-6">
            <button
              onClick={() => setShowUploadForm(!showUploadForm)}
              className="bg-primary hover:bg-primary/90 text-white py-3 px-6 rounded-lg font-semibold flex items-center gap-2"
            >
              <span className="material-symbols-outlined">add</span>
              Upload New Resource
            </button>
          </div>

          {/* Upload Form */}
          {showUploadForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm mb-6"
            >
              <h3 className="text-xl font-semibold mb-4">Upload Resource</h3>
              <form onSubmit={handleUploadResource} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Title *</label>
                  <input
                    type="text"
                    name="title"
                    value={resourceForm.title}
                    onChange={handleResourceFormChange}
                    required
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Description *</label>
                  <textarea
                    name="description"
                    value={resourceForm.description}
                    onChange={handleResourceFormChange}
                    required
                    rows={3}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Category *</label>
                    <input
                      type="text"
                      name="category"
                      value={resourceForm.category}
                      onChange={handleResourceFormChange}
                      required
                      placeholder="e.g., Python, Machine Learning"
                      className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Resource Type *</label>
                    <select
                      name="resource_type"
                      value={resourceForm.resource_type}
                      onChange={handleResourceFormChange}
                      className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                    >
                      <option value="pdf">PDF</option>
                      <option value="video">Video</option>
                      <option value="article">Article</option>
                      <option value="code">Code</option>
                      <option value="document">Document</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Tags (comma-separated)</label>
                    <input
                      type="text"
                      name="tags"
                      value={resourceForm.tags}
                      onChange={handleResourceFormChange}
                      placeholder="python, tutorial, beginner"
                      className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Difficulty Level</label>
                    <select
                      name="difficulty_level"
                      value={resourceForm.difficulty_level}
                      onChange={handleResourceFormChange}
                      className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Upload File</label>
                  <input
                    type="file"
                    onChange={handleFileChange}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">OR External URL</label>
                  <input
                    type="url"
                    name="external_url"
                    value={resourceForm.external_url}
                    onChange={handleResourceFormChange}
                    placeholder="https://example.com/resource"
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                  />
                </div>

                <div className="flex gap-3">
                  <button
                    type="submit"
                    disabled={uploading}
                    className="flex-1 bg-primary hover:bg-primary/90 text-white py-2 px-4 rounded-lg font-semibold disabled:opacity-50"
                  >
                    {uploading ? 'Uploading...' : 'Upload Resource'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowUploadForm(false)}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </motion.div>
          )}

          {/* Resources List */}
          <div className="space-y-4">
            {myResources.length === 0 ? (
              <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
                <span className="material-symbols-outlined text-6xl text-gray-400 mb-4">folder_open</span>
                <p className="text-gray-600 dark:text-gray-400">No resources uploaded yet</p>
              </div>
            ) : (
              myResources.map((resource) => (
                <motion.div
                  key={resource._id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold mb-2">{resource.title}</h3>
                      <p className="text-gray-600 dark:text-gray-400 mb-4">{resource.description}</p>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full text-sm">
                          {resource.category}
                        </span>
                        <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded-full text-sm">
                          {resource.resource_type}
                        </span>
                        <span className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-full text-sm">
                          {resource.difficulty_level}
                        </span>
                      </div>

                      <div className="flex gap-6 text-sm text-gray-500">
                        <span>👁 {resource.views || 0} views</span>
                        <span>⬇️ {resource.downloads || 0} downloads</span>
                        <span>❤️ {resource.likes?.length || 0} likes</span>
                      </div>
                    </div>

                    <button
                      onClick={() => handleDeleteResource(resource._id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <span className="material-symbols-outlined">delete</span>
                    </button>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherDashboard;
