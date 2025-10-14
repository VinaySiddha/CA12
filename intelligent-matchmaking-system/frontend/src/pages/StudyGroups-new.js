import React, { useState } from 'react';

const StudyGroups = () => {
  const [activeTab, setActiveTab] = useState('myGroups');
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  // Mock data
  const myGroups = [
    {
      id: 1,
      name: "React Advanced Patterns",
      members: 8,
      nextSession: "Tomorrow, 3:00 PM",
      topics: ["Hooks", "Context API", "Redux"],
      description: "A group for discussing advanced React patterns and state management strategies."
    },
    {
      id: 2,
      name: "Algorithm Study Group",
      members: 5,
      nextSession: "Friday, 6:00 PM",
      topics: ["Dynamic Programming", "Graph Algorithms", "Data Structures"],
      description: "Weekly algorithm challenges and discussions to improve problem-solving skills."
    }
  ];
  
  const suggestedGroups = [
    {
      id: 3,
      name: "Cloud Architecture",
      members: 12,
      topics: ["AWS", "Azure", "Serverless"],
      description: "Discussions on cloud architecture design patterns and best practices."
    },
    {
      id: 4,
      name: "Machine Learning Projects",
      members: 15,
      topics: ["TensorFlow", "PyTorch", "Data Preprocessing"],
      description: "Collaborative projects implementing various ML models and techniques."
    },
    {
      id: 5,
      name: "UI/UX Design Critique",
      members: 9,
      topics: ["User Testing", "Design Systems", "Prototyping"],
      description: "Share and receive feedback on UI/UX design work in a supportive environment."
    }
  ];
  
  return (
    <div className="px-4 py-8">
      <div className="flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Study Groups</h1>
            <p className="text-[#616b89] dark:text-white/70">
              Collaborate with peers in focused learning environments
            </p>
          </div>
          <button 
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-1 py-2 px-4 rounded-lg bg-primary text-white hover:bg-primary/90"
          >
            <span className="material-symbols-outlined">add</span>
            Create Group
          </button>
        </div>
        
        {/* Tabs */}
        <div className="flex border-b border-[#dbdee6]/20 dark:border-[#dbdee6]/10">
          <button 
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'myGroups' 
                ? 'text-primary border-b-2 border-primary' 
                : 'text-[#616b89] dark:text-white/70'
            }`}
            onClick={() => setActiveTab('myGroups')}
          >
            My Groups
          </button>
          <button 
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'discover' 
                ? 'text-primary border-b-2 border-primary' 
                : 'text-[#616b89] dark:text-white/70'
            }`}
            onClick={() => setActiveTab('discover')}
          >
            Discover
          </button>
        </div>
        
        {/* My Groups */}
        {activeTab === 'myGroups' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {myGroups.map(group => (
              <div key={group.id} className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
                <div className="flex justify-between">
                  <h2 className="font-bold text-lg">{group.name}</h2>
                  <div className="flex items-center text-sm text-[#616b89] dark:text-white/70">
                    <span className="material-symbols-outlined mr-1">people</span>
                    {group.members} members
                  </div>
                </div>
                
                <p className="text-sm">{group.description}</p>
                
                <div className="flex flex-wrap gap-2">
                  {group.topics.map(topic => (
                    <span key={topic} className="px-3 py-1 text-xs rounded-full bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white">
                      {topic}
                    </span>
                  ))}
                </div>
                
                <div className="flex items-center justify-between mt-2 pt-3 border-t border-[#dbdee6]/10 dark:border-[#dbdee6]/5">
                  <div className="flex items-center text-sm text-[#616b89] dark:text-white/70">
                    <span className="material-symbols-outlined mr-1">event</span>
                    Next: {group.nextSession}
                  </div>
                  
                  <div className="flex gap-2">
                    <button className="p-2 rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white hover:bg-white dark:hover:bg-black/30">
                      <span className="material-symbols-outlined">forum</span>
                    </button>
                    <button className="p-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20">
                      <span className="material-symbols-outlined">videocam</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
            
            {myGroups.length === 0 && (
              <div className="flex flex-col items-center justify-center p-10 col-span-2 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20">
                <span className="material-symbols-outlined text-5xl text-[#616b89] dark:text-white/50 mb-4">group_off</span>
                <h3 className="text-lg font-medium">No Study Groups Yet</h3>
                <p className="text-sm text-[#616b89] dark:text-white/70 text-center mt-2 max-w-md">
                  You haven't joined any study groups yet. Create your own or discover existing ones to collaborate with peers.
                </p>
                <button 
                  onClick={() => setActiveTab('discover')}
                  className="mt-4 py-2 px-4 text-sm font-medium rounded-lg bg-primary text-white hover:bg-primary/90"
                >
                  Discover Groups
                </button>
              </div>
            )}
          </div>
        )}
        
        {/* Discover Groups */}
        {activeTab === 'discover' && (
          <>
            <div className="max-w-xl mx-auto mb-6">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search study groups by topic, name, or description..."
                  className="w-full px-4 py-2 pl-10 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
                <span className="absolute left-3 top-2.5 text-[#616b89] dark:text-white/70">
                  <span className="material-symbols-outlined">search</span>
                </span>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {suggestedGroups.map(group => (
                <div key={group.id} className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
                  <div className="flex justify-between">
                    <h2 className="font-bold">{group.name}</h2>
                    <div className="flex items-center text-sm text-[#616b89] dark:text-white/70">
                      <span className="material-symbols-outlined mr-1">people</span>
                      {group.members}
                    </div>
                  </div>
                  
                  <p className="text-sm">{group.description}</p>
                  
                  <div className="flex flex-wrap gap-2">
                    {group.topics.map(topic => (
                      <span key={topic} className="px-3 py-1 text-xs rounded-full bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white">
                        {topic}
                      </span>
                    ))}
                  </div>
                  
                  <button className="mt-2 py-2 text-sm font-medium rounded-lg bg-primary text-white hover:bg-primary/90">
                    Join Group
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
      
      {/* Create Group Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-[#111318] rounded-xl max-w-lg w-full p-6 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Create Study Group</h2>
              <button 
                onClick={() => setShowCreateModal(false)}
                className="p-1 rounded-full hover:bg-white/10"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>
            
            <form className="space-y-4">
              <div className="flex flex-col gap-2">
                <label htmlFor="group-name" className="text-sm font-medium">Group Name</label>
                <input
                  type="text"
                  id="group-name"
                  placeholder="e.g., JavaScript Study Group"
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
              </div>
              
              <div className="flex flex-col gap-2">
                <label htmlFor="group-description" className="text-sm font-medium">Description</label>
                <textarea
                  id="group-description"
                  rows={3}
                  placeholder="What will this group focus on?"
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                ></textarea>
              </div>
              
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium">Topics</label>
                <div className="flex flex-wrap gap-2">
                  <input
                    type="text"
                    placeholder="Add topics and press Enter..."
                    className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                  />
                </div>
              </div>
              
              <div className="flex flex-col gap-2">
                <label htmlFor="group-privacy" className="text-sm font-medium">Privacy</label>
                <select
                  id="group-privacy"
                  className="w-full px-4 py-2 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
                >
                  <option value="public">Public - Anyone can join</option>
                  <option value="private">Private - By invitation only</option>
                </select>
              </div>
              
              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="py-2 px-4 rounded-lg bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white hover:bg-white dark:hover:bg-black/30"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="py-2 px-4 rounded-lg bg-primary text-white hover:bg-primary/90"
                >
                  Create Group
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudyGroups;