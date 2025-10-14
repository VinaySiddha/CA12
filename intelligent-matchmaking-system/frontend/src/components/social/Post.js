import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';

const Post = ({ post, onUpdate, onDelete }) => {
  const { user } = useAuth();
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [isLiked, setIsLiked] = useState(post.is_liked);
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [comments, setComments] = useState(post.comments || []);
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  const handleLike = async () => {
    try {
      const response = await axios.post(`/social/posts/${post.id}/like`);
      setIsLiked(response.data.is_liked);
      setLikesCount(response.data.likes_count);
    } catch (error) {
      console.error('Error toggling like:', error);
      toast.error('Failed to update like');
    }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    
    if (!commentText.trim()) {
      toast.error('Please write a comment');
      return;
    }

    setIsSubmittingComment(true);

    try {
      const response = await axios.post(`/social/posts/${post.id}/comments`, {
        content: commentText.trim(),
      });

      if (response.data.comment) {
        setComments([...comments, response.data.comment]);
        setCommentText('');
        toast.success('Comment added!');
      }
    } catch (error) {
      console.error('Error adding comment:', error);
      toast.error('Failed to add comment');
    } finally {
      setIsSubmittingComment(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return;
    }

    try {
      await axios.delete(`/social/posts/${post.id}`);
      toast.success('Post deleted successfully');
      if (onDelete) onDelete(post.id);
    } catch (error) {
      console.error('Error deleting post:', error);
      toast.error('Failed to delete post');
    }
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'teacher':
        return 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/30';
      case 'admin':
        return 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30';
      default:
        return 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/30';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md"
    >
      {/* Post Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white font-bold">
            {post.user_name.charAt(0).toUpperCase()}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-[#111318] dark:text-white">{post.user_name}</h3>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${getRoleBadgeColor(post.user_role)}`}>
                {post.user_role}
              </span>
            </div>
            <p className="text-sm text-[#616b89] dark:text-white/70">{formatDate(post.created_at)}</p>
          </div>
        </div>
        
        {user?.email === post.user_id && (
          <button
            onClick={handleDelete}
            className="text-[#616b89] dark:text-white/70 hover:text-red-500 dark:hover:text-red-400 transition-colors"
          >
            <span className="material-symbols-outlined text-xl">delete</span>
          </button>
        )}
      </div>

      {/* Post Content */}
      <div className="mb-4">
        <p className="text-[#111318] dark:text-white whitespace-pre-wrap">{post.content}</p>
      </div>

      {/* Tags */}
      {post.tags && post.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {post.tags.map((tag, index) => (
            <span
              key={index}
              className="text-xs px-2 py-1 rounded-full bg-primary/10 text-primary"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Post Actions */}
      <div className="flex items-center gap-6 pt-4 border-t border-[#dbdee6]/20 dark:border-[#dbdee6]/10">
        <button
          onClick={handleLike}
          className={`flex items-center gap-2 transition-colors ${
            isLiked
              ? 'text-red-500'
              : 'text-[#616b89] dark:text-white/70 hover:text-red-500'
          }`}
        >
          <span className="material-symbols-outlined">
            {isLiked ? 'favorite' : 'favorite_border'}
          </span>
          <span className="text-sm font-medium">{likesCount}</span>
        </button>

        <button
          onClick={() => setShowComments(!showComments)}
          className="flex items-center gap-2 text-[#616b89] dark:text-white/70 hover:text-primary transition-colors"
        >
          <span className="material-symbols-outlined">chat_bubble_outline</span>
          <span className="text-sm font-medium">{comments.length}</span>
        </button>

        <button className="flex items-center gap-2 text-[#616b89] dark:text-white/70 hover:text-primary transition-colors">
          <span className="material-symbols-outlined">share</span>
          <span className="text-sm font-medium">Share</span>
        </button>
      </div>

      {/* Comments Section */}
      <AnimatePresence>
        {showComments && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 pt-4 border-t border-[#dbdee6]/20 dark:border-[#dbdee6]/10"
          >
            {/* Comment Form */}
            <form onSubmit={handleComment} className="mb-4">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                  placeholder="Write a comment..."
                  className="flex-1 px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
                <button
                  type="submit"
                  disabled={isSubmittingComment || !commentText.trim()}
                  className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="material-symbols-outlined">send</span>
                </button>
              </div>
            </form>

            {/* Comments List */}
            <div className="space-y-3">
              {comments.map((comment) => (
                <div key={comment.id} className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                    {comment.user_name.charAt(0).toUpperCase()}
                  </div>
                  <div className="flex-1">
                    <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-sm text-[#111318] dark:text-white">
                          {comment.user_name}
                        </span>
                        <span className={`text-xs px-1.5 py-0.5 rounded border ${getRoleBadgeColor(comment.user_role)}`}>
                          {comment.user_role}
                        </span>
                      </div>
                      <p className="text-sm text-[#111318] dark:text-white">{comment.content}</p>
                    </div>
                    <p className="text-xs text-[#616b89] dark:text-white/70 mt-1 ml-3">
                      {formatDate(comment.created_at)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default Post;
