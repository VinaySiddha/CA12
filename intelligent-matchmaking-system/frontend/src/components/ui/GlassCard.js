import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

const GlassCard = ({
  children,
  className = '',
  hover = true,
  glow = false,
  padding = 'md',
  ...props
}) => {
  const baseClasses = `
    relative border border-gray-200 rounded-xl
    bg-white shadow-sm transition-all duration-300
    overflow-hidden group
  `;

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10',
  };

  const hoverClasses = hover ? `
    hover:shadow-md hover:border-gray-300
    hover:bg-gray-50
    hover:scale-[1.02] hover:-translate-y-1
  ` : '';

  const glowClasses = glow ? `
    shadow-lg hover:shadow-xl
  ` : '';

  const cardClasses = clsx(
    baseClasses,
    paddingClasses[padding],
    hoverClasses,
    glowClasses,
    className
  );

  return (
    <motion.div
      className={cardClasses}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      {...props}
    >
      {/* Glass reflection effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      {/* Subtle animated border */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary-400/0 via-primary-400/30 to-primary-400/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" style={{
        background: 'linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.3) 50%, transparent 100%)',
        mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
        maskComposite: 'xor',
        WebkitMaskComposite: 'xor',
        padding: '1px',
      }} />
      
      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
};

export default GlassCard;