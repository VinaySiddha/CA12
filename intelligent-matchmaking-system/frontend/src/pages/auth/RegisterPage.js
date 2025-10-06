import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  EyeIcon, 
  EyeSlashIcon, 
  EnvelopeIcon, 
  LockClosedIcon,
  UserIcon,
  AcademicCapIcon,
  ArrowRightIcon,
  SparklesIcon,
  CheckIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../../context/AuthContext';
import GlassCard from '../../components/ui/GlassCard';
import GlassButton from '../../components/ui/GlassButton';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';

const RegisterPage = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    // Step 1: Basic Info
    email: '',
    password: '',
    confirmPassword: '',
    
    // Step 2: Profile
    full_name: '',
    field_of_study: '',
    academic_level: '',
    university: '',
    bio: '',
    
    // Step 3: Learning Preferences
    interests: [],
    strengths: [],
    weaknesses: [],
    learning_preferences: [],
    goals: [],
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const { register, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleMultiSelectChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value],
    }));
  };

  const validateStep = (step) => {
    switch (step) {
      case 1:
        if (!formData.email || !formData.password || !formData.confirmPassword) {
          toast.error('Please fill in all required fields');
          return false;
        }
        if (formData.password !== formData.confirmPassword) {
          toast.error('Passwords do not match');
          return false;
        }
        if (formData.password.length < 6) {
          toast.error('Password must be at least 6 characters');
          return false;
        }
        return true;
      
      case 2:
        if (!formData.full_name || !formData.field_of_study || !formData.academic_level) {
          toast.error('Please fill in all required fields');
          return false;
        }
        return true;
      
      case 3:
        if (formData.interests.length === 0) {
          toast.error('Please select at least one interest');
          return false;
        }
        return true;
      
      default:
        return true;
    }
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, 3));
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateStep(3)) return;

    setIsLoading(true);
    
    try {
      const registrationData = {
        email: formData.email,
        password: formData.password,
        profile: {
          full_name: formData.full_name,
          field_of_study: formData.field_of_study,
          academic_level: formData.academic_level,
          university: formData.university,
          bio: formData.bio,
          learning_preferences: formData.learning_preferences,
          goals: formData.goals,
        },
        skills: {
          interests: formData.interests,
          strengths: formData.strengths,
          weaknesses: formData.weaknesses,
        },
      };

      const result = await register(registrationData);
      
      if (result.success) {
        navigate('/dashboard', { replace: true });
      }
    } catch (error) {
      console.error('Registration error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const inputClasses = `
    w-full px-4 py-3 rounded-lg
    bg-white/5 border border-white/20
    text-white placeholder-white/50
    focus:outline-none focus:ring-2 focus:ring-primary-400/50 focus:border-primary-400/50
    backdrop-blur-md transition-all duration-300
    hover:bg-white/10 hover:border-white/30
  `;

  const selectClasses = `
    ${inputClasses}
    appearance-none cursor-pointer
  `;

  // Options for form fields
  const academicLevels = [
    { value: '', label: 'Select Academic Level' },
    { value: 'undergraduate', label: 'Undergraduate' },
    { value: 'graduate', label: 'Graduate' },
    { value: 'phd', label: 'PhD' },
    { value: 'postdoc', label: 'Postdoc' },
  ];

  const fieldsOfStudy = [
    'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology',
    'Psychology', 'Business', 'Engineering', 'Literature', 'History',
    'Art', 'Music', 'Philosophy', 'Political Science', 'Economics',
  ];

  const availableInterests = [
    'Machine Learning', 'Data Science', 'Web Development', 'Mobile Development',
    'Artificial Intelligence', 'Cybersecurity', 'Cloud Computing', 'DevOps',
    'Database Design', 'UI/UX Design', 'Game Development', 'Blockchain',
    'Statistics', 'Research Methods', 'Technical Writing', 'Public Speaking',
  ];

  const learningPrefs = [
    { value: 'visual', label: 'Visual Learning' },
    { value: 'auditory', label: 'Auditory Learning' },
    { value: 'kinesthetic', label: 'Hands-on Learning' },
    { value: 'reading', label: 'Reading/Writing' },
  ];

  const renderStep1 = () => (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Create Account</h2>
        <p className="text-white/70">Let's get started with your basic information</p>
      </div>

      {/* Email */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Email Address *
        </label>
        <div className="relative">
          <EnvelopeIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="Enter your email"
            className={`${inputClasses} pl-12`}
            required
          />
        </div>
      </div>

      {/* Password */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Password *
        </label>
        <div className="relative">
          <LockClosedIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
          <input
            type={showPassword ? 'text' : 'password'}
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            placeholder="Create a strong password"
            className={`${inputClasses} pl-12 pr-12`}
            required
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white/50 hover:text-white/80"
          >
            {showPassword ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Confirm Password */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Confirm Password *
        </label>
        <div className="relative">
          <LockClosedIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
          <input
            type={showConfirmPassword ? 'text' : 'password'}
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            placeholder="Confirm your password"
            className={`${inputClasses} pl-12 pr-12`}
            required
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white/50 hover:text-white/80"
          >
            {showConfirmPassword ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Profile Information</h2>
        <p className="text-white/70">Tell us about your academic background</p>
      </div>

      {/* Full Name */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Full Name *
        </label>
        <div className="relative">
          <UserIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleInputChange}
            placeholder="Enter your full name"
            className={`${inputClasses} pl-12`}
            required
          />
        </div>
      </div>

      {/* Field of Study */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Field of Study *
        </label>
        <select
          name="field_of_study"
          value={formData.field_of_study}
          onChange={handleInputChange}
          className={selectClasses}
          required
        >
          <option value="">Select your field of study</option>
          {fieldsOfStudy.map(field => (
            <option key={field} value={field} className="bg-dark-800 text-white">
              {field}
            </option>
          ))}
        </select>
      </div>

      {/* Academic Level */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Academic Level *
        </label>
        <select
          name="academic_level"
          value={formData.academic_level}
          onChange={handleInputChange}
          className={selectClasses}
          required
        >
          {academicLevels.map(level => (
            <option key={level.value} value={level.value} className="bg-dark-800 text-white">
              {level.label}
            </option>
          ))}
        </select>
      </div>

      {/* University */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          University/Institution
        </label>
        <div className="relative">
          <AcademicCapIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
          <input
            type="text"
            name="university"
            value={formData.university}
            onChange={handleInputChange}
            placeholder="Enter your university or institution"
            className={`${inputClasses} pl-12`}
          />
        </div>
      </div>

      {/* Bio */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Bio (Optional)
        </label>
        <textarea
          name="bio"
          value={formData.bio}
          onChange={handleInputChange}
          placeholder="Tell us a bit about yourself and your learning goals..."
          className={`${inputClasses} h-20 resize-none`}
          rows={3}
        />
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Learning Preferences</h2>
        <p className="text-white/70">Help us match you with the perfect study partners</p>
      </div>

      {/* Interests */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-3">
          Interests * (Select at least one)
        </label>
        <div className="grid grid-cols-2 gap-2">
          {availableInterests.map(interest => (
            <button
              key={interest}
              type="button"
              onClick={() => handleMultiSelectChange('interests', interest)}
              className={`
                px-3 py-2 rounded-lg text-sm transition-all duration-300
                ${formData.interests.includes(interest)
                  ? 'bg-primary-500/80 text-white border-primary-400'
                  : 'bg-white/5 text-white/70 border-white/20 hover:bg-white/10 hover:text-white'
                }
                border backdrop-blur-md
              `}
            >
              {formData.interests.includes(interest) && (
                <CheckIcon className="w-4 h-4 inline mr-1" />
              )}
              {interest}
            </button>
          ))}
        </div>
      </div>

      {/* Learning Preferences */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-3">
          Learning Style Preferences
        </label>
        <div className="grid grid-cols-2 gap-2">
          {learningPrefs.map(pref => (
            <button
              key={pref.value}
              type="button"
              onClick={() => handleMultiSelectChange('learning_preferences', pref.value)}
              className={`
                px-3 py-2 rounded-lg text-sm transition-all duration-300
                ${formData.learning_preferences.includes(pref.value)
                  ? 'bg-secondary-500/80 text-white border-secondary-400'
                  : 'bg-white/5 text-white/70 border-white/20 hover:bg-white/10 hover:text-white'
                }
                border backdrop-blur-md
              `}
            >
              {formData.learning_preferences.includes(pref.value) && (
                <CheckIcon className="w-4 h-4 inline mr-1" />
              )}
              {pref.label}
            </button>
          ))}
        </div>
      </div>

      {/* Goals */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Learning Goals (Optional)
        </label>
        <textarea
          name="goals"
          value={formData.goals.join('\n')}
          onChange={(e) => setFormData(prev => ({ ...prev, goals: e.target.value.split('\n').filter(g => g.trim()) }))}
          placeholder="Enter your learning goals (one per line)&#10;Example:&#10;Master machine learning algorithms&#10;Improve presentation skills&#10;Learn data visualization"
          className={`${inputClasses} h-24 resize-none`}
          rows={4}
        />
      </div>
    </div>
  );

  const renderStepIndicator = () => (
    <div className="flex items-center justify-center mb-8">
      {[1, 2, 3].map((step) => (
        <div key={step} className="flex items-center">
          <div
            className={`
              w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium
              transition-all duration-300
              ${step <= currentStep
                ? 'bg-primary-500 text-white shadow-glow-sm'
                : 'bg-white/10 text-white/50'
              }
            `}
          >
            {step < currentStep ? (
              <CheckIcon className="w-5 h-5" />
            ) : (
              step
            )}
          </div>
          {step < 3 && (
            <div
              className={`
                w-16 h-1 mx-2 rounded-full transition-all duration-300
                ${step < currentStep ? 'bg-primary-500' : 'bg-white/20'}
              `}
            />
          )}
        </div>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4">
      <motion.div
        className="w-full max-w-2xl"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <motion.div
            className="inline-flex items-center justify-center w-16 h-16 bg-gradient-primary rounded-full mb-4 shadow-glow-md"
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          >
            <SparklesIcon className="w-8 h-8 text-white" />
          </motion.div>
          
          <h1 className="text-3xl font-bold text-white mb-2">
            Join LearnTogether
          </h1>
          <p className="text-white/70">
            Create your account and start collaborating with amazing learners
          </p>
        </div>

        <GlassCard>
          {renderStepIndicator()}
          
          <form onSubmit={handleSubmit}>
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {currentStep === 1 && renderStep1()}
              {currentStep === 2 && renderStep2()}
              {currentStep === 3 && renderStep3()}
            </motion.div>

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              {currentStep > 1 ? (
                <GlassButton
                  type="button"
                  onClick={prevStep}
                  variant="ghost"
                >
                  ← Previous
                </GlassButton>
              ) : (
                <div />
              )}

              {currentStep < 3 ? (
                <GlassButton
                  type="button"
                  onClick={nextStep}
                  variant="primary"
                  className="group"
                >
                  Next
                  <ArrowRightIcon className="w-4 h-4 ml-2 transition-transform group-hover:translate-x-1" />
                </GlassButton>
              ) : (
                <GlassButton
                  type="submit"
                  variant="primary"
                  disabled={isLoading}
                  loading={isLoading}
                  className="group"
                >
                  {isLoading ? 'Creating Account...' : (
                    <>
                      Create Account
                      <SparklesIcon className="w-4 h-4 ml-2 transition-transform group-hover:rotate-12" />
                    </>
                  )}
                </GlassButton>
              )}
            </div>
          </form>
        </GlassCard>

        {/* Sign In Link */}
        <motion.div
          className="text-center mt-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <p className="text-white/70">
            Already have an account?{' '}
            <Link
              to="/login"
              className="text-primary-400 hover:text-primary-300 transition-colors font-medium"
            >
              Sign in
            </Link>
          </p>
        </motion.div>

        {/* Back to Home */}
        <motion.div
          className="text-center mt-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <Link
            to="/"
            className="inline-flex items-center text-white/60 hover:text-white/80 transition-colors"
          >
            ← Back to Home
          </Link>
        </motion.div>
      </motion.div>

      {/* Floating Background Elements */}
      <div className="fixed top-10 right-10 w-32 h-32 bg-primary-500/10 rounded-full blur-xl animate-pulse" />
      <div className="fixed bottom-10 left-10 w-40 h-40 bg-secondary-500/10 rounded-full blur-xl animate-pulse" style={{ animationDelay: '1s' }} />
      <div className="fixed top-1/3 right-1/4 w-20 h-20 bg-accent-500/10 rounded-full blur-xl animate-pulse" style={{ animationDelay: '2s' }} />
    </div>
  );
};

export default RegisterPage;