import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Matches = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('suggestions');
  
  // Mock data for demonstrations
  const suggestedMatches = [
    {
      id: 1,
      name: "Alex Johnson",
      role: "Frontend Developer",
      compatibility: 98,
      interests: ["React", "UI/UX", "JavaScript"],
      bio: "Passionate about creating beautiful and functional web interfaces. Looking for peers to discuss advanced React patterns."
    },
    {
      id: 2,
      name: "Sarah Williams",
      role: "Data Scientist",
      compatibility: 92,
      interests: ["Python", "Machine Learning", "Data Visualization"],
      bio: "Working on ML projects and always excited to collaborate with others on interesting data challenges."
    },
    {
      id: 3,
      name: "Michael Chen",
      role: "Full Stack Developer",
      compatibility: 87,
      interests: ["Node.js", "MongoDB", "TypeScript"],
      bio: "Building scalable applications and interested in system design. Would love to connect with fellow developers."
    }
  ];
  
  const activeMatches = [
    {
      id: 4,
      name: "Emma Davis",
      role: "UX Designer",
      lastActivity: "2 days ago",
      interests: ["Design Systems", "Figma", "User Research"],
      bio: "Collaborating on design systems and accessibility improvements."
    },
    {
      id: 5,
      name: "David Rodriguez",
      role: "Backend Engineer",
      lastActivity: "Just now",
      interests: ["Java", "Spring Boot", "Microservices"],
      bio: "Working together on API design and performance optimization."
    }
  ];
  
  return (
    <div className="px-4 py-8">
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-bold">Your Matches</h1>
          <p className="text-[#616b89] dark:text-white/70">
            Connect with peers who match your skills, interests, and learning goals.
          </p>
        </div>
        
        {/* Tabs */}
        <div className="flex border-b border-[#dbdee6]/20 dark:border-[#dbdee6]/10">
          <button 
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'suggestions' 
                ? 'text-primary border-b-2 border-primary' 
                : 'text-[#616b89] dark:text-white/70'
            }`}
            onClick={() => setActiveTab('suggestions')}
          >
            Suggested Matches
          </button>
          <button 
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'active' 
                ? 'text-primary border-b-2 border-primary' 
                : 'text-[#616b89] dark:text-white/70'
            }`}
            onClick={() => setActiveTab('active')}
          >
            Active Connections
          </button>
        </div>
        
        {/* Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {activeTab === 'suggestions' ? (
            suggestedMatches.map(match => (
              <div key={match.id} className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#8A2BE2]/20 to-[#4B0082]/20 flex items-center justify-center">
                    <span className="material-symbols-outlined">person</span>
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between">
                      <h2 className="font-bold">{match.name}</h2>
                      <span className="text-sm font-medium text-primary">{match.compatibility}% Match</span>
                    </div>
                    <p className="text-sm text-[#616b89] dark:text-white/70">{match.role}</p>
                  </div>
                </div>
                
                <p className="text-sm">{match.bio}</p>
                
                <div className="flex flex-wrap gap-2">
                  {match.interests.map(interest => (
                    <span key={interest} className="px-3 py-1 text-xs rounded-full bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white">
                      {interest}
                    </span>
                  ))}
                </div>
                
                <div className="flex gap-3 mt-2">
                  <button className="flex-1 py-2 text-sm font-medium rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white hover:bg-white dark:hover:bg-black/30">
                    Skip
                  </button>
                  <button className="flex-1 py-2 text-sm font-medium rounded-lg bg-primary text-white hover:bg-primary/90">
                    Connect
                  </button>
                </div>
              </div>
            ))
          ) : (
            activeMatches.map(match => (
              <div key={match.id} className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#8A2BE2]/20 to-[#4B0082]/20 flex items-center justify-center">
                    <span className="material-symbols-outlined">person</span>
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between">
                      <h2 className="font-bold">{match.name}</h2>
                      <span className="text-xs text-[#616b89] dark:text-white/70">Active {match.lastActivity}</span>
                    </div>
                    <p className="text-sm text-[#616b89] dark:text-white/70">{match.role}</p>
                  </div>
                </div>
                
                <p className="text-sm">{match.bio}</p>
                
                <div className="flex flex-wrap gap-2">
                  {match.interests.map(interest => (
                    <span key={interest} className="px-3 py-1 text-xs rounded-full bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white">
                      {interest}
                    </span>
                  ))}
                </div>
                
                <div className="flex gap-3 mt-2">
                  <button className="flex-1 py-2 text-sm font-medium rounded-lg bg-primary/10 text-primary hover:bg-primary/20 flex items-center justify-center">
                    <span className="material-symbols-outlined mr-1">calendar_today</span>
                    Schedule
                  </button>
                  <button className="flex-1 py-2 text-sm font-medium rounded-lg bg-primary text-white hover:bg-primary/90 flex items-center justify-center">
                    <span className="material-symbols-outlined mr-1">chat</span>
                    Message
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
        
        {/* If no matches */}
        {((activeTab === 'suggestions' && suggestedMatches.length === 0) || 
          (activeTab === 'active' && activeMatches.length === 0)) && (
          <div className="flex flex-col items-center justify-center p-10 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20">
            <span className="material-symbols-outlined text-5xl text-[#616b89] dark:text-white/50 mb-4">search</span>
            <h3 className="text-lg font-medium">No matches found</h3>
            <p className="text-sm text-[#616b89] dark:text-white/70 text-center mt-2 max-w-md">
              {activeTab === 'suggestions' 
                ? "We're looking for your perfect matches. Check back soon!" 
                : "You haven't connected with anyone yet. Try reaching out to your suggested matches."}
            </p>
            {activeTab === 'active' && (
              <button className="mt-4 py-2 px-4 text-sm font-medium rounded-lg bg-primary text-white hover:bg-primary/90">
                Find Matches
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Matches;