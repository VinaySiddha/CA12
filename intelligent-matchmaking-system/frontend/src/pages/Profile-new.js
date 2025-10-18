import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    bio: user?.bio || '',
    educational_level: user?.educational_level || '',
    field_of_study: user?.field_of_study || '',
    institution: user?.institution || '',
    learning_style: user?.learning_style || '',
    interests: user?.interests || [],
  });
  
  // Educational levels
  const educationalLevels = [
    'High School',
    'Associate Degree',
    "Bachelor's Degree",
    "Master's Degree",
    'PhD',
    'Self-taught',
    'Other'
  ];
  
  // Fields of study
  const fieldsOfStudy = [
    'Computer Science',
    'Data Science',
    'Engineering',
    'Mathematics',
    'Business',
    'Arts',
    'Humanities',
    'Medicine',
    'Law',
    'Other'
  ];
  
  // Learning styles
  const learningStyles = [
    'Visual',
    'Auditory',
    'Reading/Writing',
    'Kinesthetic',
    'Multimodal',
  ];
  
  // Common interests
  const commonInterests = [
    'Programming',
    'Web Development',
    'Data Science',
    'AI/ML',
    'Mobile Development',
    'DevOps',
    'Cloud Computing',
    'Design',
    'Project Management',
    'Security',
    'Blockchain',
  ];
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  
  const handleInterestToggle = (interest) => {
    if (formData.interests.includes(interest)) {
      setFormData({
        ...formData,
        interests: formData.interests.filter((item) => item !== interest),
      });
    } else {
      setFormData({
        ...formData,
        interests: [...formData.interests, interest],
      });
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Structure the data to match backend schema
      const updateData = {
        full_name: formData.full_name,
        profile: {
          bio: formData.bio,
          academic_level: formData.educational_level,
          field_of_study: formData.field_of_study,
          learning_preferences: [formData.learning_style],
          institution: formData.institution,
          timezone: 'UTC',
          languages: ['English']
        },
        skills: {
          interests: formData.interests,
          strengths: [],
          weaknesses: [],
          expertise_level: {}
        }
      };
      
      const result = await updateUser(updateData);
      if (result.success) {
        toast.success('Profile updated successfully');
        setIsEditing(false);
      } else {
        toast.error('Failed to update profile');
      }
    } catch (error) {
      toast.error(error.message || 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="px-4 py-8">
      <div className="flex flex-col gap-6 max-w-3xl mx-auto">
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">Your Profile</h1>
            {!isEditing ? (
              <button 
                onClick={() => setIsEditing(true)}
                className="flex items-center gap-1 py-2 px-4 rounded-lg bg-primary/10 text-primary hover:bg-primary/20"
              >
                <span className="material-symbols-outlined">edit</span>
                Edit Profile
              </button>
            ) : (
              <button 
                onClick={() => setIsEditing(false)}
                className="flex items-center gap-1 py-2 px-4 rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white"
              >
                <span className="material-symbols-outlined">close</span>
                Cancel
              </button>
            )}
          </div>
          <p className="text-[#616b89] dark:text-white/70">
            Manage your personal information and preferences
          </p>
        </div>
        
        <div className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
          {!isEditing ? (
            <div className="flex flex-col gap-8">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-[#8A2BE2]/20 to-[#4B0082]/20 flex items-center justify-center">
                  <span className="material-symbols-outlined" style={{ fontSize: '40px' }}>person</span>
                </div>
                <div>
                  <h2 className="text-xl font-bold">{user?.full_name}</h2>
                  <p className="text-[#616b89] dark:text-white/70">{user?.email}</p>
                  <div className="flex gap-2 mt-2">
                    <span className="px-3 py-1 text-xs rounded-full bg-primary/10 text-primary">
                      {user?.field_of_study || 'Field not specified'}
                    </span>
                    <span className="px-3 py-1 text-xs rounded-full bg-primary/10 text-primary">
                      {user?.educational_level || 'Education not specified'}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="font-medium mb-2">About Me</h3>
                  <p className="text-[#616b89] dark:text-white/70">{user?.bio || 'No bio provided'}</p>
                </div>
                
                <div>
                  <h3 className="font-medium mb-2">Learning Style</h3>
                  <p className="text-[#616b89] dark:text-white/70">{user?.learning_style || 'Not specified'}</p>
                </div>
                
                <div>
                  <h3 className="font-medium mb-2">Interests</h3>
                  {user?.interests?.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {user.interests.map(interest => (
                        <span key={interest} className="px-3 py-1 text-xs rounded-full bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white">
                          {interest}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-[#616b89] dark:text-white/70">No interests specified</p>
                  )}
                </div>
                
                <div>
                  <h3 className="font-medium mb-2">Account Stats</h3>
                  <div className="flex gap-4">
                    <div className="flex flex-col items-center p-3 rounded-lg bg-white/50 dark:bg-black/20">
                      <span className="text-xl font-bold">12</span>
                      <span className="text-xs text-[#616b89] dark:text-white/70">Connections</span>
                    </div>
                    <div className="flex flex-col items-center p-3 rounded-lg bg-white/50 dark:bg-black/20">
                      <span className="text-xl font-bold">5</span>
                      <span className="text-xs text-[#616b89] dark:text-white/70">Sessions</span>
                    </div>
                    <div className="flex flex-col items-center p-3 rounded-lg bg-white/50 dark:bg-black/20">
                      <span className="text-xl font-bold">95%</span>
                      <span className="text-xs text-[#616b89] dark:text-white/70">Rating</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col gap-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label htmlFor="full_name" className="text-sm font-medium">Full Name</label>
                  <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  />
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="email" className="text-sm font-medium">Email</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    disabled
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50 opacity-70"
                  />
                </div>
                
                <div className="flex flex-col gap-2 md:col-span-2">
                  <label htmlFor="bio" className="text-sm font-medium">About Me</label>
                  <textarea
                    id="bio"
                    name="bio"
                    value={formData.bio}
                    onChange={handleChange}
                    rows={4}
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                    placeholder="Tell others about yourself..."
                  ></textarea>
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="educational_level" className="text-sm font-medium">Education Level</label>
                  <select
                    id="educational_level"
                    name="educational_level"
                    value={formData.educational_level}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  >
                    <option value="" disabled>Select your education level</option>
                    {educationalLevels.map((level) => (
                      <option key={level} value={level}>{level}</option>
                    ))}
                  </select>
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="field_of_study" className="text-sm font-medium">Field of Study</label>
                  <select
                    id="field_of_study"
                    name="field_of_study"
                    value={formData.field_of_study}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  >
                    <option value="" disabled>Select your field of study</option>
                    {fieldsOfStudy.map((field) => (
                      <option key={field} value={field}>{field}</option>
                    ))}
                  </select>
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="institution" className="text-sm font-medium">Institution</label>
                  <input
                    id="institution"
                    name="institution"
                    type="text"
                    value={formData.institution}
                    onChange={handleChange}
                    placeholder="University or Institution name"
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  />
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="learning_style" className="text-sm font-medium">Learning Style</label>
                  <select
                    id="learning_style"
                    name="learning_style"
                    value={formData.learning_style}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  >
                    <option value="" disabled>Select your learning style</option>
                    {learningStyles.map((style) => (
                      <option key={style} value={style}>{style}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium">Interests</label>
                <div className="flex flex-wrap gap-2">
                  {commonInterests.map((interest) => (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => handleInterestToggle(interest)}
                      className={`px-3 py-1.5 text-xs rounded-full ${
                        formData.interests.includes(interest)
                          ? 'bg-primary text-white'
                          : 'bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white'
                      }`}
                    >
                      {interest}
                    </button>
                  ))}
                </div>
              </div>
              
              <div className="flex justify-end gap-3 mt-4">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="py-2 px-6 rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white hover:bg-white dark:hover:bg-black/30"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="py-2 px-6 rounded-lg bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
                >
                  {isLoading ? (
                    <span className="material-symbols-outlined animate-spin">progress_activity</span>
                  ) : 'Save Changes'}
                </button>
              </div>
            </form>
          )}
        </div>
        
        <div className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
          <h2 className="text-lg font-bold mb-4">Account Settings</h2>
          
          <div className="flex flex-col gap-4">
            <div className="flex justify-between items-center p-4 border-b border-[#dbdee6]/10 dark:border-[#dbdee6]/5">
              <div>
                <h3 className="font-medium">Change Password</h3>
                <p className="text-sm text-[#616b89] dark:text-white/70">Update your password regularly for security</p>
              </div>
              <button className="py-1.5 px-3 rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white hover:bg-white dark:hover:bg-black/30 text-sm">
                Change
              </button>
            </div>
            
            <div className="flex justify-between items-center p-4 border-b border-[#dbdee6]/10 dark:border-[#dbdee6]/5">
              <div>
                <h3 className="font-medium">Notification Preferences</h3>
                <p className="text-sm text-[#616b89] dark:text-white/70">Manage how you receive notifications</p>
              </div>
              <button className="py-1.5 px-3 rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white hover:bg-white dark:hover:bg-black/30 text-sm">
                Manage
              </button>
            </div>
            
            <div className="flex justify-between items-center p-4">
              <div>
                <h3 className="font-medium text-red-500">Delete Account</h3>
                <p className="text-sm text-[#616b89] dark:text-white/70">Permanently delete your account and data</p>
              </div>
              <button className="py-1.5 px-3 rounded-lg bg-red-500/10 text-red-500 hover:bg-red-500/20 text-sm">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;