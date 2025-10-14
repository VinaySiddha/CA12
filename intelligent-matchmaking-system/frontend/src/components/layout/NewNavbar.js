import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const NewNavbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
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

  const handleLogout = () => {
    logout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  return (
    <header className="flex items-center justify-between border-b border-solid border-b-[#f0f1f4]/10 dark:border-b-[#f0f1f4]/10 px-4 md:px-10 py-3 fixed top-0 left-0 right-0 w-full bg-background-light/95 dark:bg-background-dark/95 backdrop-blur-md z-50 shadow-sm">
      <div className="flex items-center gap-2 md:gap-4 text-primary">
        <div className="size-5 md:size-6 flex-shrink-0">
          <svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path clipRule="evenodd" d="M24 4H6V17.3333V30.6667H24V44H42V30.6667V17.3333H24V4Z" fillRule="evenodd"></path>
          </svg>
        </div>
        <h2 className="text-[#111318] dark:text-white text-sm md:text-lg font-bold leading-tight tracking-[-0.015em] truncate">
          Intelligent Peer Matchmaking
        </h2>
      </div>
      
      {/* Desktop Navigation */}
      <div className="hidden lg:flex flex-1 justify-end gap-6">
        <div className="flex items-center gap-6">
          {!isAuthenticated ? (
            <>
              <Link to="/" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">About</Link>
              <Link to="/services" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">Services</Link>
              <Link to="/projects" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">Projects</Link>
              <Link to="/contact" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">Contact</Link>
            </>
          ) : (
            <>
              <Link to="/dashboard" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">Dashboard</Link>
              <Link to="/matches" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">Matches</Link>
              
              {/* Teacher-specific links */}
              {user?.role === 'teacher' && (
                <Link to="/teacher/students" className="text-purple-600 dark:text-purple-400 text-sm font-medium leading-normal hover:text-purple-700 dark:hover:text-purple-300 transition-colors">Students</Link>
              )}
              
              {/* Admin-specific links */}
              {user?.role === 'admin' && (
                <Link to="/admin" className="text-amber-600 dark:text-amber-400 text-sm font-medium leading-normal hover:text-amber-700 dark:hover:text-amber-300 transition-colors">Admin</Link>
              )}
              
              <Link to="/profile" className="text-[#111318] dark:text-white text-sm font-medium leading-normal hover:text-primary transition-colors">Profile</Link>
            </>
          )}
        </div>
        <div className="flex gap-2">
          {!isAuthenticated ? (
            <>
              <Link to="/login" className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 text-primary text-sm font-bold leading-normal hover:bg-primary/10 transition-colors">
                <span className="truncate">Login</span>
              </Link>
              <Link to="/register" className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 bg-primary text-white text-sm font-bold leading-normal hover:bg-primary/90 transition-colors">
                <span className="truncate">Sign Up</span>
              </Link>
            </>
          ) : (
            <button
              onClick={handleLogout}
              className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 bg-primary text-white text-sm font-bold leading-normal hover:bg-primary/90 transition-colors"
            >
              <span className="truncate">Logout</span>
            </button>
          )}
        </div>
      </div>
      
      {/* Mobile Menu Button */}
      <button
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        className="lg:hidden flex items-center justify-center w-10 h-10 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        aria-label="Toggle menu"
      >
        <span className="material-symbols-outlined text-[#111318] dark:text-white">
          {mobileMenuOpen ? 'close' : 'menu'}
        </span>
      </button>
      
      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden absolute top-full left-0 right-0 bg-white dark:bg-gray-900 border-b border-[#f0f1f4]/10 dark:border-[#f0f1f4]/10 shadow-lg">
          <div className="flex flex-col py-4 px-4 gap-3">
            {!isAuthenticated ? (
              <>
                <Link to="/" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">About</Link>
                <Link to="/services" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Services</Link>
                <Link to="/projects" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Projects</Link>
                <Link to="/contact" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Contact</Link>
                <div className="flex flex-col gap-2 mt-4 pt-4 border-t border-[#f0f1f4]/10">
                  <Link to="/login" onClick={() => setMobileMenuOpen(false)} className="flex items-center justify-center rounded-lg h-10 px-4 text-primary text-sm font-bold hover:bg-primary/10 transition-colors">
                    Login
                  </Link>
                  <Link to="/register" onClick={() => setMobileMenuOpen(false)} className="flex items-center justify-center rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold hover:bg-primary/90 transition-colors">
                    Sign Up
                  </Link>
                </div>
              </>
            ) : (
              <>
                <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Dashboard</Link>
                <Link to="/matches" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Matches</Link>
                <Link to="/study-groups" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Study Groups</Link>
                <Link to="/resources" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Resources</Link>
                
                {user?.role === 'teacher' && (
                  <>
                    <div className="mt-2 pt-2 border-t border-[#f0f1f4]/10">
                      <p className="text-xs font-semibold text-purple-600 dark:text-purple-400 mb-2">Teacher Tools</p>
                      <Link to="/teacher/students" onClick={() => setMobileMenuOpen(false)} className="text-purple-600 dark:text-purple-400 text-sm font-medium py-2 block hover:text-purple-700 transition-colors">My Students</Link>
                      <Link to="/teacher/create-groups" onClick={() => setMobileMenuOpen(false)} className="text-purple-600 dark:text-purple-400 text-sm font-medium py-2 block hover:text-purple-700 transition-colors">Create Groups</Link>
                      <Link to="/teacher/feedback" onClick={() => setMobileMenuOpen(false)} className="text-purple-600 dark:text-purple-400 text-sm font-medium py-2 block hover:text-purple-700 transition-colors">Feedback</Link>
                    </div>
                  </>
                )}
                
                {user?.role === 'admin' && (
                  <div className="mt-2 pt-2 border-t border-[#f0f1f4]/10">
                    <p className="text-xs font-semibold text-amber-600 dark:text-amber-400 mb-2">Administration</p>
                    <Link to="/admin" onClick={() => setMobileMenuOpen(false)} className="text-amber-600 dark:text-amber-400 text-sm font-medium py-2 block hover:text-amber-700 transition-colors">Admin Panel</Link>
                  </div>
                )}
                
                <Link to="/profile" onClick={() => setMobileMenuOpen(false)} className="text-[#111318] dark:text-white text-sm font-medium py-2 hover:text-primary transition-colors">Profile</Link>
                
                <button
                  onClick={handleLogout}
                  className="mt-4 flex items-center justify-center rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold hover:bg-primary/90 transition-colors"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default NewNavbar;