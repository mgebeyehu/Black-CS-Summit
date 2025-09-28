import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Policy } from '../types';
import { FileText, ArrowRight } from 'lucide-react';

interface PolicyListProps {
  policies: Policy[];
  onPolicySelect: (policy: Policy) => void;
}

const PolicyList: React.FC<PolicyListProps> = ({ policies, onPolicySelect }) => {
  const navigate = useNavigate();

  const handlePolicyClick = (policy: Policy) => {
    onPolicySelect(policy);
    navigate('/chat');
  };

  const groupedPolicies = policies.reduce((acc, policy) => {
    if (!acc[policy.category]) {
      acc[policy.category] = [];
    }
    acc[policy.category].push(policy);
    return acc;
  }, {} as Record<string, Policy[]>);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Policies That May Affect You
          </h1>
          <p className="text-xl text-gray-600">
            Based on your profile, here are Chicago policies and regulations that could impact your life.
          </p>
        </div>

        <div className="space-y-8">
          {Object.entries(groupedPolicies).map(([category, categoryPolicies]) => (
            <div key={category} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4 capitalize">
                {category.replace(/([A-Z])/g, ' $1').trim()}
              </h2>
              <div className="grid gap-4">
                {categoryPolicies.map((policy) => (
                  <div
                    key={policy.id}
                    onClick={() => handlePolicyClick(policy)}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 cursor-pointer transition-colors group"
                  >
                    <div className="flex items-start space-x-3">
                      <FileText className="h-5 w-5 text-gray-400 mt-1 group-hover:text-blue-600" />
                      <div>
                        <h3 className="font-medium text-gray-900 group-hover:text-blue-700">
                          {policy.title}
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">
                          {policy.description}
                        </p>
                        <div className="flex items-center mt-2">
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                            {Math.round(policy.relevanceScore * 100)}% relevant
                          </span>
                        </div>
                      </div>
                    </div>
                    <ArrowRight className="h-5 w-5 text-gray-400 group-hover:text-blue-600" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PolicyList;