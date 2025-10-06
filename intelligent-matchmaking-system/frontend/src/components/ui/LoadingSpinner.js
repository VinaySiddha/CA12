import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

const LoadingSpinner = ({ 
  size = 'md', 
  color = 'primary', 
  className = '',
  text = '',
  overlay = false 
}) => {
  const sizes = {
    xs: 'w-4 h-4',
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  const colors = {
    primary: 'border-primary-500',
    secondary: 'border-secondary-500',
    accent: 'border-accent-500',
    white: 'border-white',
    gray: 'border-gray-500',
  };

  const spinnerClasses = clsx(
    'animate-spin rounded-full border-2 border-transparent',
    sizes[size],
    className
  );

  const borderClasses = clsx(
    'border-t-2',
    colors[color]
  );

  const spinner = (
    <div className="flex flex-col items-center space-y-4">
      <motion.div
        className={spinnerClasses}
        style={{
          borderTopColor: 'currentColor',
          borderRightColor: 'transparent',
          borderBottomColor: 'transparent',
          borderLeftColor: 'transparent',
        }}
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: 'linear',
        }}
      >
        <div className={`${borderClasses} absolute inset-0 rounded-full`} />
      </motion.div>
      
      {text && (
        <motion.p
          className="text-sm text-white/70 font-medium"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {text}
        </motion.p>
      )}
    </div>
  );

  if (overlay) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="glass-card p-8">
          {spinner}
        </div>
      </div>
    );
  }

  return spinner;
};

export default LoadingSpinner;