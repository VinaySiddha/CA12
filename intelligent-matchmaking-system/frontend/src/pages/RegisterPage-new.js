import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

const RegisterPage = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    // Step 1: Basic Info
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    role: 'student', // Default role
    
    // Step 2: Profile
    full_name: '',
    educational_level: '',
    field_of_study: '',
    
    // Step 3: Interests & Goals
    interests: [],
    learning_goals: [],
    learning_style: '',
    
    // Teacher specific fields
    teaching_subjects: [],
    years_experience: '',
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const { register, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);
  
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  
  const nextStep = () => {
    if (currentStep === 1) {
      // Validate email, username and passwords
      if (!formData.email || !formData.username || !formData.password || !formData.confirmPassword) {
        toast.error('Please fill in all required fields');
        return;
      }
      
      if (formData.password !== formData.confirmPassword) {
        toast.error('Passwords do not match');
        return;
      }
      
      if (formData.password.length < 6) {
        toast.error('Password must be at least 6 characters');
        return;
      }
      
      if (formData.username.length < 3) {
        toast.error('Username must be at least 3 characters');
        return;
      }
    }
    
    if (currentStep === 2) {
      // Validate profile info
      if (!formData.full_name || !formData.educational_level || !formData.field_of_study) {
        toast.error('Please fill in all required fields');
        return;
      }
    }
    
    setCurrentStep(currentStep + 1);
  };
  
  const prevStep = () => {
    setCurrentStep(currentStep - 1);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Don't remove confirmPassword - it's needed for auto-login
      const result = await register(formData);
      
      if (result.success) {
        if (result.requiresLogin) {
          // Registration succeeded but auto-login failed, redirect to login
          toast.success('Registration successful! Please log in.');
          navigate('/login');
        } else {
          // Both registration and auto-login succeeded
          toast.success('Registration successful!');
          navigate('/dashboard');
        }
      } else {
        toast.error(result.error || 'Registration failed');
      }
    } catch (error) {
      toast.error(error.message || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };
  
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
  
  // Subject options for teachers
  const teachingSubjects = [
    'Computer Science', 
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'English',
    'History',
    'Economics',
    'Business',
    'Psychology',
    'Programming',
    'Web Development',
    'Data Science',
    'Machine Learning'
  ];
  
  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-center">Account Information</h2>
            <p className="text-sm text-center text-[#616b89] dark:text-white/70 mb-6">Create your account credentials</p>
            
            {/* Account Type Selection */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium">Account Type</label>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setFormData({...formData, role: 'student'})}
                  className={`flex-1 py-2 px-3 rounded-lg border transition-all ${
                    formData.role === 'student' 
                      ? 'bg-primary text-white border-primary' 
                      : 'bg-white/50 dark:bg-black/20 border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <span className="material-symbols-outlined">school</span>
                    <span>Student</span>
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({...formData, role: 'teacher'})}
                  className={`flex-1 py-2 px-3 rounded-lg border transition-all ${
                    formData.role === 'teacher' 
                      ? 'bg-primary text-white border-primary' 
                      : 'bg-white/50 dark:bg-black/20 border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <span className="material-symbols-outlined">history_edu</span>
                    <span>Teacher</span>
                  </div>
                </button>
              </div>
            </div>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="email" className="text-sm font-medium">Email Address</label>
              <div className="relative">
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="your@email.com"
                />
                <span className="absolute right-3 top-2.5 text-[#616b89] dark:text-white/70">
                  <span className="material-symbols-outlined">mail</span>
                </span>
              </div>
            </div>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="username" className="text-sm font-medium">Username</label>
              <div className="relative">
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="username"
                />
                <span className="absolute right-3 top-2.5 text-[#616b89] dark:text-white/70">
                  <span className="material-symbols-outlined">person</span>
                </span>
              </div>
            </div>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="password" className="text-sm font-medium">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="••••••••"
                />
                <button 
                  type="button"
                  onClick={togglePasswordVisibility}
                  className="absolute right-3 top-2.5 text-[#616b89] dark:text-white/70"
                >
                  <span className="material-symbols-outlined">
                    {showPassword ? 'visibility_off' : 'visibility'}
                  </span>
                </button>
              </div>
            </div>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="confirmPassword" className="text-sm font-medium">Confirm Password</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="••••••••"
                />
                <button 
                  type="button"
                  onClick={togglePasswordVisibility}
                  className="absolute right-3 top-2.5 text-[#616b89] dark:text-white/70"
                >
                  <span className="material-symbols-outlined">
                    {showPassword ? 'visibility_off' : 'visibility'}
                  </span>
                </button>
              </div>
            </div>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-center">Personal Profile</h2>
            <p className="text-sm text-center text-[#616b89] dark:text-white/70 mb-6">Tell us a bit about yourself</p>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="full_name" className="text-sm font-medium">Full Name</label>
              <div className="relative">
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="Your full name"
                />
                <span className="absolute right-3 top-2.5 text-[#616b89] dark:text-white/70">
                  <span className="material-symbols-outlined">person</span>
                </span>
              </div>
            </div>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="educational_level" className="text-sm font-medium">Education Level</label>
              <select
                id="educational_level"
                name="educational_level"
                value={formData.educational_level}
                onChange={handleChange}
                required
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
                required
                className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                <option value="" disabled>Select your field of study</option>
                {fieldsOfStudy.map((field) => (
                  <option key={field} value={field}>{field}</option>
                ))}
              </select>
            </div>
          </div>
        );
        
      case 3:
        return (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-center">
              {formData.role === 'teacher' ? 'Teaching Profile' : 'Interests & Learning Style'}
            </h2>
            <p className="text-sm text-center text-[#616b89] dark:text-white/70 mb-6">
              {formData.role === 'teacher' 
                ? 'Tell us about your teaching experience' 
                : 'Help us match you with like-minded peers'}
            </p>
            
            {formData.role === 'teacher' ? (
              <>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium">Subjects You Teach</label>
                  <div className="flex flex-wrap gap-2">
                    {teachingSubjects.map((subject) => (
                      <button
                        key={subject}
                        type="button"
                        onClick={() => {
                          const subjects = formData.teaching_subjects || [];
                          if (subjects.includes(subject)) {
                            setFormData({
                              ...formData, 
                              teaching_subjects: subjects.filter(s => s !== subject)
                            });
                          } else {
                            setFormData({
                              ...formData,
                              teaching_subjects: [...subjects, subject]
                            });
                          }
                        }}
                        className={`px-3 py-1 text-sm rounded-full transition-all ${
                          formData.teaching_subjects?.includes(subject)
                            ? 'bg-primary text-white'
                            : 'bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white'
                        }`}
                      >
                        {subject}
                      </button>
                    ))}
                  </div>
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="years_experience" className="text-sm font-medium">Years of Teaching Experience</label>
                  <input
                    type="number"
                    id="years_experience"
                    name="years_experience"
                    value={formData.years_experience}
                    onChange={handleChange}
                    min="0"
                    max="50"
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  />
                </div>
              </>
            ) : (
              <>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium">Technical Interests</label>
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
            
                <div className="flex flex-col gap-2">
                  <label htmlFor="learning_style" className="text-sm font-medium">Preferred Learning Style</label>
                  <select
                    id="learning_style"
                    name="learning_style"
                    value={formData.learning_style}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  >
                    <option value="" disabled>Select your learning style</option>
                    {learningStyles.map((style) => (
                      <option key={style} value={style}>{style}</option>
                    ))}
                  </select>
                </div>
                
                <div className="flex flex-col gap-2">
                  <label htmlFor="learning_goals" className="text-sm font-medium">Learning Goals</label>
                  <textarea
                    id="learning_goals"
                    name="learning_goals"
                    value={formData.learning_goals}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                    placeholder="What do you hope to achieve through peer learning?"
                    rows={3}
                  />
                </div>
              </>
            )}
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <div className="flex flex-col items-center justify-center px-4 py-16">
      <div className="w-full max-w-md">
        <div className="flex flex-col gap-6 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-8 backdrop-blur-md">
          {/* Progress Steps */}
          <div className="flex items-center justify-between mb-4">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex flex-col items-center">
                <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                  currentStep >= step
                    ? 'bg-primary text-white'
                    : 'bg-white dark:bg-gray-700 text-gray-500'
                }`}>
                  {currentStep > step ? (
                    <span className="material-symbols-outlined text-sm">check</span>
                  ) : (
                    step
                  )}
                </div>
                <span className="text-xs mt-1 text-[#616b89] dark:text-white/70">
                  {step === 1 ? 'Account' : step === 2 ? 'Profile' : 'Interests'}
                </span>
              </div>
            ))}
          </div>
          
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {renderStep()}
            
            <div className="flex justify-between mt-6">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={prevStep}
                  className="flex items-center px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white hover:bg-white/50 dark:hover:bg-black/20"
                >
                  <span className="material-symbols-outlined mr-1">arrow_back</span>
                  Back
                </button>
              )}
              
              {currentStep < 3 ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="flex items-center ml-auto px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90"
                >
                  Next
                  <span className="material-symbols-outlined ml-1">arrow_forward</span>
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex items-center ml-auto px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
                >
                  {isLoading ? (
                    <span className="material-symbols-outlined animate-spin mr-2">progress_activity</span>
                  ) : null}
                  Complete Registration
                </button>
              )}
            </div>
          </form>
          
          <div className="mt-4 text-center text-sm text-[#616b89] dark:text-white/70">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:underline">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;