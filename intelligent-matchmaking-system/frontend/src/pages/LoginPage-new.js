import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  const from = location.state?.from?.pathname || '/dashboard';
  
  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await login(formData.email, formData.password);
      toast.success('Login successful');
      navigate(from, { replace: true });
    } catch (error) {
      toast.error(error.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleDemoLogin = async (role) => {
    setIsLoading(true);
    let email, password;
    
    switch(role) {
      case 'student':
        email = 'student@example.com';
        password = 'student123';
        break;
      case 'teacher':
        email = 'teacher@example.com';
        password = 'teacher123';
        break;
      case 'admin':
        email = 'admin@example.com';
        password = 'admin123';
        break;
      default:
        email = 'student@example.com';
        password = 'student123';
    }
    
    try {
      await login(email, password);
      toast.success(`Logged in as ${role}`);
      navigate(from, { replace: true });
    } catch (error) {
      toast.error(error.message || 'Demo login failed');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex flex-col items-center justify-center px-4 py-16">
      <div className="w-full max-w-md">
        <div className="flex flex-col gap-6 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-8 backdrop-blur-md">
          <div className="text-center mb-4">
            <h1 className="text-[#111318] dark:text-white text-2xl font-bold mb-2">Welcome Back</h1>
            <p className="text-[#616b89] dark:text-white/70 text-sm">Sign in to your account to continue</p>
          </div>
          
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <label htmlFor="email" className="text-sm font-medium text-[#111318] dark:text-white">Email</label>
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
              <label htmlFor="password" className="text-sm font-medium text-[#111318] dark:text-white">Password</label>
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
            
            <div className="flex items-center justify-between mt-2">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-primary rounded border-[#dbdee6]/30 dark:border-[#dbdee6]/10"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-[#616b89] dark:text-white/70">
                  Remember me
                </label>
              </div>
              <div className="text-sm">
                <a href="#" className="text-primary hover:underline">
                  Forgot your password?
                </a>
              </div>
            </div>
            
            <button
              type="submit"
              disabled={isLoading}
              className="mt-6 flex w-full justify-center items-center rounded-lg bg-primary py-2.5 px-4 text-white hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <span className="material-symbols-outlined animate-spin mr-2">progress_activity</span>
              ) : null}
              Sign in
            </button>
          </form>
          
          <div className="mt-4 text-center text-sm text-[#616b89] dark:text-white/70">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary hover:underline">
              Sign up now
            </Link>
          </div>
          
          <div className="mt-8 pt-6 border-t border-[#dbdee6]/20 dark:border-[#dbdee6]/10">
            <h3 className="text-center text-sm font-medium text-[#111318] dark:text-white mb-4">
              Quick Demo Access
            </h3>
            <div className="grid grid-cols-3 gap-3">
              <button
                onClick={() => handleDemoLogin('student')}
                disabled={isLoading}
                className="flex flex-col items-center justify-center p-3 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 text-blue-600 border border-blue-500/30 transition-colors"
              >
                <span className="material-symbols-outlined mb-1">school</span>
                <span className="text-xs font-medium">Student</span>
              </button>
              
              <button
                onClick={() => handleDemoLogin('teacher')}
                disabled={isLoading}
                className="flex flex-col items-center justify-center p-3 rounded-lg bg-purple-500/10 hover:bg-purple-500/20 text-purple-600 border border-purple-500/30 transition-colors"
              >
                <span className="material-symbols-outlined mb-1">history_edu</span>
                <span className="text-xs font-medium">Teacher</span>
              </button>
              
              <button
                onClick={() => handleDemoLogin('admin')}
                disabled={isLoading}
                className="flex flex-col items-center justify-center p-3 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-600 border border-amber-500/30 transition-colors"
              >
                <span className="material-symbols-outlined mb-1">admin_panel_settings</span>
                <span className="text-xs font-medium">Admin</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;