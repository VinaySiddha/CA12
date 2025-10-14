import React, { useState } from 'react';

const Resources = () => {
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Mock data for resources
  const resourcesData = [
    {
      id: 1,
      title: "Modern JavaScript: From Fundamentals to Advanced",
      type: "course",
      category: "web-development",
      rating: 4.8,
      author: "Alex Johnson",
      description: "Comprehensive JavaScript course covering everything from basic syntax to advanced topics like closures, promises, and async/await.",
      tags: ["JavaScript", "ES6", "Web Development"]
    },
    {
      id: 2,
      title: "Data Structures and Algorithms in Python",
      type: "ebook",
      category: "programming",
      rating: 4.7,
      author: "Dr. Maria Rodriguez",
      description: "A practical guide to implementing the most important data structures and algorithms in Python with real-world applications.",
      tags: ["Python", "Algorithms", "Data Structures"]
    },
    {
      id: 3,
      title: "Introduction to Machine Learning",
      type: "video",
      category: "ai-ml",
      rating: 4.9,
      author: "Prof. John Smith",
      description: "Clear and concise introduction to machine learning concepts, including supervised and unsupervised learning techniques.",
      tags: ["Machine Learning", "AI", "Data Science"]
    },
    {
      id: 4,
      title: "React Hooks: Complete Reference",
      type: "article",
      category: "web-development",
      rating: 4.6,
      author: "Sarah Chen",
      description: "In-depth guide to all React hooks with practical examples and best practices for state management.",
      tags: ["React", "JavaScript", "Web Development"]
    },
    {
      id: 5,
      title: "Cloud Architecture Patterns",
      type: "ebook",
      category: "cloud",
      rating: 4.7,
      author: "Michael Brown",
      description: "Essential patterns for designing resilient, scalable, and cost-effective cloud solutions on any platform.",
      tags: ["Cloud", "Architecture", "AWS", "Azure"]
    },
    {
      id: 6,
      title: "Mobile App Development with Flutter",
      type: "course",
      category: "mobile",
      rating: 4.8,
      author: "David Kim",
      description: "Learn how to build cross-platform mobile applications using Flutter and Dart programming language.",
      tags: ["Flutter", "Mobile", "Dart", "Cross-platform"]
    }
  ];
  
  const categories = [
    { id: 'all', name: 'All Resources' },
    { id: 'web-development', name: 'Web Development' },
    { id: 'programming', name: 'Programming' },
    { id: 'ai-ml', name: 'AI & Machine Learning' },
    { id: 'cloud', name: 'Cloud Computing' },
    { id: 'mobile', name: 'Mobile Development' }
  ];
  
  const resourceTypes = [
    { id: 'course', icon: 'school', color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' },
    { id: 'ebook', icon: 'book', color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400' },
    { id: 'video', icon: 'play_circle', color: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400' },
    { id: 'article', icon: 'article', color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400' },
  ];
  
  // Filter resources based on category and search query
  const filteredResources = resourcesData.filter(resource => {
    const matchesCategory = activeCategory === 'all' || resource.category === activeCategory;
    const matchesSearch = searchQuery === '' || 
      resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      resource.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      resource.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    
    return matchesCategory && matchesSearch;
  });
  
  const getResourceTypeInfo = (type) => {
    return resourceTypes.find(t => t.id === type) || { icon: 'description', color: 'bg-gray-100 text-gray-600 dark:bg-gray-900/30 dark:text-gray-400' };
  };
  
  return (
    <div className="px-4 py-8">
      <div className="flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-bold">Learning Resources</h1>
          <p className="text-[#616b89] dark:text-white/70">
            Discover curated resources to enhance your learning journey
          </p>
        </div>
        
        {/* Search and Filter */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search resources..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 pl-10 rounded-lg border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
            <span className="absolute left-3 top-2.5 text-[#616b89] dark:text-white/70">
              <span className="material-symbols-outlined">search</span>
            </span>
          </div>
          <div className="flex overflow-x-auto gap-2 pb-2 no-scrollbar">
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`px-4 py-2 text-sm font-medium rounded-lg whitespace-nowrap ${
                  activeCategory === category.id
                    ? 'bg-primary text-white'
                    : 'bg-white/50 dark:bg-black/20 text-[#111318] dark:text-white'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>
        
        {/* Resources Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredResources.map(resource => {
            const typeInfo = getResourceTypeInfo(resource.type);
            
            return (
              <div key={resource.id} className="flex flex-col rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 overflow-hidden backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:shadow-primary/5 hover:border-primary/50 dark:hover:border-primary/50">
                <div className="p-6 flex flex-col gap-4 flex-1">
                  <div className="flex items-start justify-between">
                    <div className={`p-2 rounded-lg ${typeInfo.color}`}>
                      <span className="material-symbols-outlined">{typeInfo.icon}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="material-symbols-outlined text-yellow-400 text-sm">star</span>
                      <span className="ml-1 text-sm font-medium">{resource.rating}</span>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-bold text-lg">{resource.title}</h3>
                    <p className="text-sm text-[#616b89] dark:text-white/70">By {resource.author}</p>
                  </div>
                  
                  <p className="text-sm flex-1">{resource.description}</p>
                  
                  <div className="flex flex-wrap gap-2">
                    {resource.tags.map(tag => (
                      <span key={tag} className="px-3 py-1 text-xs rounded-full bg-white/50 dark:bg-black/20 border border-[#dbdee6]/30 dark:border-[#dbdee6]/10 text-[#111318] dark:text-white">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="flex border-t border-[#dbdee6]/10 dark:border-[#dbdee6]/5">
                  <button className="flex-1 py-3 text-center text-sm font-medium hover:bg-white/50 dark:hover:bg-black/20 text-[#111318] dark:text-white">
                    Save
                  </button>
                  <div className="w-px bg-[#dbdee6]/10 dark:bg-[#dbdee6]/5"></div>
                  <button className="flex-1 py-3 text-center text-sm font-medium text-primary hover:bg-primary/5">
                    Access Resource
                  </button>
                </div>
              </div>
            );
          })}
        </div>
        
        {filteredResources.length === 0 && (
          <div className="flex flex-col items-center justify-center p-10 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20">
            <span className="material-symbols-outlined text-5xl text-[#616b89] dark:text-white/50 mb-4">search_off</span>
            <h3 className="text-lg font-medium">No resources found</h3>
            <p className="text-sm text-[#616b89] dark:text-white/70 text-center mt-2 max-w-md">
              We couldn't find any resources matching your current filters. Try adjusting your search or category selection.
            </p>
            <button 
              onClick={() => {
                setActiveCategory('all');
                setSearchQuery('');
              }}
              className="mt-4 py-2 px-4 text-sm font-medium rounded-lg bg-primary text-white hover:bg-primary/90"
            >
              Clear Filters
            </button>
          </div>
        )}
        
        {/* Submit Resource */}
        <div className="mt-6 rounded-xl p-8 bg-gradient-to-r from-primary to-[#8A2BE2] text-center flex flex-col items-center gap-4">
          <h2 className="text-white text-xl font-bold">Have a valuable resource to share?</h2>
          <p className="text-white/80 text-sm max-w-xl">
            Contribute to our community by sharing high-quality learning resources that have helped you in your journey.
          </p>
          <button className="mt-2 py-2.5 px-6 rounded-lg bg-white text-primary text-sm font-medium hover:bg-white/90">
            Submit a Resource
          </button>
        </div>
      </div>
    </div>
  );
};

export default Resources;