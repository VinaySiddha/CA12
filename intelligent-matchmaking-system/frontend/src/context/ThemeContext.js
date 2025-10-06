import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    // Check local storage first
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    
    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    
    return 'light';
  });

  const [accentColor, setAccentColor] = useState(() => {
    return localStorage.getItem('accentColor') || 'blue';
  });

  // Update document class and local storage when theme changes
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Update accent color in local storage
  useEffect(() => {
    localStorage.setItem('accentColor', accentColor);
    // Update CSS custom properties for accent color
    const root = document.documentElement;
    
    const colors = {
      blue: {
        50: '#eff6ff',
        100: '#dbeafe',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
      },
      purple: {
        50: '#faf5ff',
        100: '#f3e8ff',
        500: '#a855f7',
        600: '#9333ea',
        700: '#7c3aed',
      },
      pink: {
        50: '#fdf2f8',
        100: '#fce7f3',
        500: '#ec4899',
        600: '#db2777',
        700: '#be185d',
      },
      green: {
        50: '#f0fdf4',
        100: '#dcfce7',
        500: '#22c55e',
        600: '#16a34a',
        700: '#15803d',
      },
      orange: {
        50: '#fff7ed',
        100: '#ffedd5',
        500: '#f59e0b',
        600: '#d97706',
        700: '#b45309',
      },
    };

    const selectedColors = colors[accentColor] || colors.blue;
    
    Object.entries(selectedColors).forEach(([shade, color]) => {
      root.style.setProperty(`--accent-${shade}`, color);
    });
  }, [accentColor]);

  // Listen for system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  const changeAccentColor = (color) => {
    setAccentColor(color);
  };

  const isDark = theme === 'dark';

  const value = {
    theme,
    isDark,
    accentColor,
    toggleTheme,
    changeAccentColor,
    setTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};