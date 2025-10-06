import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  EyeIcon, 
  EyeSlashIcon, 
  EnvelopeIcon, 
  LockClosedIcon,
  ArrowRightIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../../context/AuthContext';
import GlassCard from '../../components/ui/GlassCard';
import GlassButton from '../../components/ui/GlassButton';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: 'alice.johnson@university.edu', // Test user
    password: 'password123', // Default password
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  const from = location.state?.from?.pathname || '/dashboard';

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      toast.error('Please fill in all fields');
      return;
    }

    setIsLoading(true);
    
    try {
      const result = await login(formData.email, formData.password);
      
      if (result.success) {
        navigate(from, { replace: true });
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const inputClasses = `
    w-full px-4 py-3 pl-12 rounded-lg
    bg-white/5 border border-white/20
    text-white placeholder-white/50
    focus:outline-none focus:ring-2 focus:ring-primary-400/50 focus:border-primary-400/50
    backdrop-blur-md transition-all duration-300
    hover:bg-white/10 hover:border-white/30
  `;

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4">
      <motion.div
        className="w-full max-w-md"
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
            Welcome Back
          </h1>
          <p className="text-white/70">
            Sign in to continue your learning journey
          </p>
        </div>

        <GlassCard>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div className="relative">
              <label htmlFor="email" className="block text-sm font-medium text-white/80 mb-2">
                Email Address
              </label>
              <div className="relative">
                <EnvelopeIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Enter your email"
                  className={inputClasses}
                  required
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="relative">
              <label htmlFor="password" className="block text-sm font-medium text-white/80 mb-2">
                Password
              </label>
              <div className="relative">
                <LockClosedIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Enter your password"
                  className={inputClasses}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white/50 hover:text-white/80 transition-colors"
                >
                  {showPassword ? (
                    <EyeSlashIcon className="w-5 h-5" />
                  ) : (
                    <EyeIcon className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-primary-500 bg-white/10 border-white/30 rounded focus:ring-primary-400/50 focus:ring-2"
                />
                <span className="ml-2 text-sm text-white/70">Remember me</span>
              </label>
              
              <Link
                to="/forgot-password"
                className="text-sm text-primary-400 hover:text-primary-300 transition-colors"
              >
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <GlassButton
              type="submit"
              variant="primary"
              className="w-full group"
              disabled={isLoading}
              loading={isLoading}
            >
              {isLoading ? (
                'Signing in...'
              ) : (
                <>
                  Sign In
                  <ArrowRightIcon className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
                </>
              )}
            </GlassButton>

            {/* Demo Accounts */}
            <div className="pt-4 border-t border-white/20">
              <p className="text-sm text-white/60 text-center mb-3">
                Quick Demo Access
              </p>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={() => setFormData({ email: 'alice.johnson@university.edu', password: 'password123' })}
                  className="px-3 py-2 text-xs bg-white/5 border border-white/20 rounded-lg text-white/70 hover:bg-white/10 hover:text-white transition-all"
                >
                  Student Demo
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ email: 'admin@learntogether.com', password: 'admin123' })}
                  className="px-3 py-2 text-xs bg-white/5 border border-white/20 rounded-lg text-white/70 hover:bg-white/10 hover:text-white transition-all"
                >
                  Admin Demo
                </button>
              </div>
            </div>
          </form>
        </GlassCard>

        {/* Sign Up Link */}
        <motion.div
          className="text-center mt-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <p className="text-white/70">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="text-primary-400 hover:text-primary-300 transition-colors font-medium"
            >
              Create one now
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
      <div className="fixed top-20 left-10 w-32 h-32 bg-primary-500/10 rounded-full blur-xl animate-pulse" />
      <div className="fixed bottom-20 right-10 w-40 h-40 bg-secondary-500/10 rounded-full blur-xl animate-pulse" style={{ animationDelay: '1s' }} />
      <div className="fixed top-1/2 left-1/4 w-20 h-20 bg-accent-500/10 rounded-full blur-xl animate-pulse" style={{ animationDelay: '2s' }} />
    </div>
  );
};

export default LoginPage;