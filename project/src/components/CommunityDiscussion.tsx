import React, { useState } from 'react';
import { DiscussionThread } from '../types';
import { MessageSquare, Users, Clock, ArrowUp, ArrowDown, Plus, Search } from 'lucide-react';

interface CommunityDiscussionProps {
  policyTitle?: string;
}

const CommunityDiscussion: React.FC<CommunityDiscussionProps> = ({ policyTitle }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const mockThreads: DiscussionThread[] = [
    {
      id: '1',
      title: 'New rent control ordinance - what does this mean for tenants?',
      author: 'ChicagoRenter23',
      replies: 45,
      lastActivity: '2 hours ago',
      category: 'Housing'
    },
    {
      id: '2',
      title: 'Small business licensing changes in 2025',
      author: 'LocalBizOwner',
      replies: 23,
      lastActivity: '4 hours ago',
      category: 'Business'
    },
    {
      id: '3',
      title: 'CTA fare increases - impact on low-income residents',
      author: 'TransitAdvocate',
      replies: 67,
      lastActivity: '6 hours ago',
      category: 'Transportation'
    },
    {
      id: '4',
      title: 'Cannabis dispensary zoning rules in residential areas',
      author: 'NeighborhoodWatch',
      replies: 89,
      lastActivity: '1 day ago',
      category: 'Zoning'
    }
  ];

  const categories = ['all', 'Housing', 'Business', 'Transportation', 'Zoning', 'Healthcare', 'Education'];

  const filteredThreads = mockThreads.filter(thread => {
    const matchesSearch = thread.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || thread.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleCreatePost = () => {
    alert('To create a new discussion, you need admin approval. Please contact our moderators.');
  };

  const handleReply = () => {
    alert('To participate in discussions, you need admin approval. Please contact our moderators to get verified.');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Community Discussions</h1>
              {policyTitle && (
                <p className="text-gray-600 mt-2">Discussing: {policyTitle}</p>
              )}
            </div>
            <button
              onClick={handleCreatePost}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <Plus className="h-4 w-4" />
              <span>New Discussion</span>
            </button>
          </div>

          {/* Search and Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search discussions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Discussion Threads */}
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          {/* Notice */}
          <div className="bg-yellow-50 border-b border-yellow-200 p-4">
            <div className="flex items-center space-x-2">
              <Users className="h-5 w-5 text-yellow-600" />
              <p className="text-sm text-yellow-800">
                <strong>Community Guidelines:</strong> To participate in discussions, you need admin approval. 
                This ensures quality conversations and prevents misinformation. Contact our moderators to get verified.
              </p>
            </div>
          </div>

          {/* Thread List */}
          <div className="divide-y divide-gray-100">
            {filteredThreads.map((thread) => (
              <div key={thread.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">
                        {thread.category}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600 cursor-pointer">
                      {thread.title}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span>by {thread.author}</span>
                      <div className="flex items-center space-x-1">
                        <MessageSquare className="h-4 w-4" />
                        <span>{thread.replies} replies</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="h-4 w-4" />
                        <span>{thread.lastActivity}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col items-center space-y-1 ml-4">
                    <button 
                      onClick={handleReply}
                      className="p-1 hover:bg-gray-200 rounded transition-colors"
                    >
                      <ArrowUp className="h-4 w-4 text-gray-400" />
                    </button>
                    <span className="text-sm font-medium text-gray-600">24</span>
                    <button 
                      onClick={handleReply}
                      className="p-1 hover:bg-gray-200 rounded transition-colors"
                    >
                      <ArrowDown className="h-4 w-4 text-gray-400" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredThreads.length === 0 && (
            <div className="p-12 text-center">
              <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No discussions found</h3>
              <p className="text-gray-600">Try adjusting your search or category filter.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CommunityDiscussion;