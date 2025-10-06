import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

const GlassButton = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  className = '',
  ...props
}) => {
  const baseClasses = `
    relative inline-flex items-center justify-center font-semibold rounded-lg
    transition-all duration-200 ease-out
    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent
    disabled:opacity-50 disabled:cursor-not-allowed
    border
    hover:scale-105 active:scale-95
    group overflow-hidden
  `;

  const variants = {
    primary: `
      bg-primary-500 hover:bg-primary-600
      border-primary-500 hover:border-primary-600
      text-white shadow-sm hover:shadow-md
      focus:ring-primary-400/50
    `,
    secondary: `
      bg-white hover:bg-gray-50
      border-primary-500 hover:border-primary-600
      text-primary-500 hover:text-primary-600 shadow-sm hover:shadow-md
      focus:ring-primary-400/50
    `,
    accent: `
      bg-accent-500 hover:bg-accent-600
      border-accent-500 hover:border-accent-600
      text-white shadow-sm hover:shadow-md
      focus:ring-accent-400/50
    `,
    ghost: `
      bg-transparent hover:bg-gray-50
      border-gray-300 hover:border-gray-400
      text-gray-700 hover:text-black shadow-sm hover:shadow-md
      focus:ring-gray-400/50
    `,
    danger: `
      bg-red-500 hover:bg-red-600
      border-red-500 hover:border-red-600
      text-white shadow-sm hover:shadow-md
      focus:ring-red-400/50
    `,
    success: `
      bg-green-500 hover:bg-green-600
      border-green-500 hover:border-green-600
      text-white shadow-sm hover:shadow-md
      focus:ring-green-400/50
    `,
    outline: `
      bg-transparent hover:bg-gray-50
      border-2 border-gray-300 hover:border-gray-400
      text-gray-700 hover:text-black
      focus:ring-gray-400/50
      focus:ring-white/30
    `,
  };

  const sizes = {
    xs: 'px-2 py-1 text-xs',
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
    xl: 'px-8 py-4 text-xl',
  };

  const buttonClasses = clsx(
    baseClasses,
    variants[variant],
    sizes[size],
    className
  );

  const buttonContent = (
    <>
      {/* Simple hover overlay effect */}
      <div className="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
      
      {/* Content */}
      <span className="relative z-10 flex items-center space-x-2">
        {loading && (
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        )}
        {children}
      </span>
    </>
  );

  return (
    <motion.button
      type={type}
      className={buttonClasses}
      disabled={disabled || loading}
      onClick={onClick}
      whileHover={{ scale: disabled ? 1 : 1.05 }}
      whileTap={{ scale: disabled ? 1 : 0.95 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      {...props}
    >
      {buttonContent}
    </motion.button>
  );
};

export default GlassButton;