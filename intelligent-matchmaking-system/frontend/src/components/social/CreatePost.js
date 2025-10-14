import React, { useState } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import axios from 'axios';

const CreatePost = ({ onPostCreated }) => {
  const [content, setContent] = useState('');
  const [tags, setTags] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!content.trim()) {
      toast.error('Please write something to post');
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await axios.post('/social/posts', {
        content: content.trim(),
        tags: tags.split(',').map(t => t.trim()).filter(t => t),
      });

      if (response.data) {
        toast.success('Post created successfully!');
        setContent('');
        setTags('');
        if (onPostCreated) onPostCreated();
      }
    } catch (error) {
      console.error('Error creating post:', error);
      toast.error(error.response?.data?.detail || 'Failed to create post');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md mb-6"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="What's on your mind? Share your thoughts, questions, or insights..."
            className="w-full px-4 py-3 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none"
            rows="4"
            maxLength={1000}
          />
          <div className="text-right text-xs text-[#616b89] dark:text-white/70 mt-1">
            {content.length}/1000
          </div>
        </div>

        <div>
          <input
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="Add tags (comma separated, e.g., programming, web-dev, python)"
            className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>

        <div className="flex justify-end gap-3">
          <button
            type="button"
            onClick={() => {
              setContent('');
              setTags('');
            }}
            className="px-4 py-2 rounded-lg text-[#616b89] dark:text-white/70 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            Clear
          </button>
          <button
            type="submit"
            disabled={isSubmitting || !content.trim()}
            className="flex items-center gap-2 px-6 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? (
              <>
                <span className="material-symbols-outlined animate-spin">progress_activity</span>
                Posting...
              </>
            ) : (
              <>
                <span className="material-symbols-outlined">send</span>
                Post
              </>
            )}
          </button>
        </div>
      </form>
    </motion.div>
  );
};

export default CreatePost;
