import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  HomeIcon, 
  UserIcon, 
  UsersIcon, 
  BookOpenIcon, 
  AcademicCapIcon,
  ChatBubbleLeftRightIcon,
  Cog6ToothIcon,
  Bars3Icon,
  XMarkIcon,
  ArrowRightOnRectangleIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import GlassButton from './ui/GlassButton';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Navigation items for authenticated users
  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Matches', href: '/matches', icon: UsersIcon },
    { name: 'Study Groups', href: '/study-groups', icon: AcademicCapIcon },
    { name: 'Resources', href: '/resources', icon: BookOpenIcon },
    { name: 'Feedback', href: '/feedback', icon: ChatBubbleLeftRightIcon },
  ];

  // Admin items
  const adminItems = [
    { name: 'Admin', href: '/admin', icon: ChartBarIcon },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const NavLink = ({ item, mobile = false }) => {
    const isActive = location.pathname === item.href;
    const Icon = item.icon;

    return (
      <Link
        to={item.href}
        onClick={() => mobile && setIsMenuOpen(false)}
        className={`
          flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-300
          ${mobile ? 'w-full' : ''}
          ${isActive 
            ? 'bg-primary-100 text-primary-700 shadow-lg border border-primary-200'
            : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
          }
        `}
      >
        <Icon className="w-5 h-5" />
        <span className="font-medium">{item.name}</span>
      </Link>
    );
  };

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className={`
          fixed top-0 left-0 right-0 z-50 transition-all duration-300
          ${scrolled 
            ? 'backdrop-blur-md bg-white/95 shadow-lg border-b border-gray-200' 
            : 'backdrop-blur-sm bg-white/90'
          }
        `}
      >
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link 
              to="/" 
              className="flex items-center space-x-3 text-gray-800 hover:text-primary-500 transition-colors"
            >
              <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center shadow-lg">
                <AcademicCapIcon className="w-6 h-6 text-black" />
              </div>
              <span className="text-xl font-bold text-gray-800">
                LearnTogether
              </span>
            </Link>

            {/* Desktop Navigation */}
            {isAuthenticated && (
              <div className="hidden md:flex items-center space-x-6">
                {navItems.map((item) => (
                  <NavLink key={item.name} item={item} />
                ))}
                
                {user?.role === 'admin' && adminItems.map((item) => (
                  <NavLink key={item.name} item={item} />
                ))}
              </div>
            )}

            {/* Right side actions */}
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  {/* Profile & Logout */}
                  <div className="hidden md:flex items-center space-x-3">
                    <Link
                      to="/profile"
                      className="flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-all"
                    >
                      <UserIcon className="w-5 h-5" />
                      <span className="font-medium">
                        {user?.profile?.full_name || 'Profile'}
                      </span>
                    </Link>
                    
                    <GlassButton
                      onClick={handleLogout}
                      size="sm"
                      variant="danger"
                      className="flex items-center space-x-2"
                    >
                      <ArrowRightOnRectangleIcon className="w-4 h-4" />
                      <span>Logout</span>
                    </GlassButton>
                  </div>

                  {/* Mobile menu button */}
                  <button
                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                    className="md:hidden p-2 rounded-lg glass-button text-black"
                  >
                    {isMenuOpen ? (
                      <XMarkIcon className="w-6 h-6" />
                    ) : (
                      <Bars3Icon className="w-6 h-6" />
                    )}
                  </button>
                </>
              ) : (
                <div className="hidden md:flex items-center space-x-3">
                  <Link to="/login">
                    <GlassButton variant="ghost" size="sm">
                      Login
                    </GlassButton>
                  </Link>
                  <Link to="/register">
                    <GlassButton variant="primary" size="sm">
                      Get Started
                    </GlassButton>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-white/10 backdrop-blur-md bg-dark-900/90"
            >
              <div className="container mx-auto px-4 py-4 space-y-2">
                {isAuthenticated ? (
                  <>
                    {navItems.map((item) => (
                      <NavLink key={item.name} item={item} mobile />
                    ))}
                    
                    {user?.role === 'admin' && adminItems.map((item) => (
                      <NavLink key={item.name} item={item} mobile />
                    ))}
                    
                    <div className="pt-4 border-t border-white/10 space-y-2">
                      <Link
                        to="/profile"
                        onClick={() => setIsMenuOpen(false)}
                        className="flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-all w-full"
                      >
                        <UserIcon className="w-5 h-5" />
                        <span className="font-medium">
                          {user?.profile?.full_name || 'Profile'}
                        </span>
                      </Link>
                      
                      <button
                        onClick={handleLogout}
                        className="flex items-center space-x-2 px-3 py-2 rounded-lg text-red-300 hover:text-red-200 hover:bg-red-500/10 transition-all w-full"
                      >
                        <ArrowRightOnRectangleIcon className="w-5 h-5" />
                        <span className="font-medium">Logout</span>
                      </button>
                    </div>
                  </>
                ) : (
                  <div className="space-y-2">
                    <Link
                      to="/login"
                      onClick={() => setIsMenuOpen(false)}
                      className="block w-full"
                    >
                      <GlassButton variant="ghost" className="w-full justify-center">
                        Login
                      </GlassButton>
                    </Link>
                    <Link
                      to="/register"
                      onClick={() => setIsMenuOpen(false)}
                      className="block w-full"
                    >
                      <GlassButton variant="primary" className="w-full justify-center">
                        Get Started
                      </GlassButton>
                    </Link>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.nav>

      {/* Spacer for fixed navbar */}
      <div className="h-16"></div>
    </>
  );
};

export default Navbar;