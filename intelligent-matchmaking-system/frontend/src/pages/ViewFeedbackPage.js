import React from 'react';
import { motion } from 'framer-motion';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/ui/GlassCard';

const ViewFeedbackPage = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-white p-6 space-y-8">
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">
          <span className="bg-gradient-to-r from-purple-500 to-purple-700 bg-clip-text text-transparent">
            Student Feedback
          </span>
        </h1>
        <p className="text-xl text-gray-600">
          Review feedback and improve your teaching
        </p>
      </motion.div>
      
      <div className="max-w-4xl mx-auto">
        <GlassCard>
          <div className="p-6 text-center">
            <ChatBubbleLeftRightIcon className="w-16 h-16 mx-auto mb-4 text-purple-500" />
            <h2 className="text-2xl font-bold text-black mb-2">Teacher-Only View</h2>
            <p className="text-gray-600">
              This page is only accessible to teachers. Here you would see student feedback,
              ratings, and suggestions to help improve your teaching methods.
            </p>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default ViewFeedbackPage;