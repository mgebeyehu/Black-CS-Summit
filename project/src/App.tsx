import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Scale, BookOpen, Users, Search, ArrowRight, Shield, Lightbulb, MessageSquare, Vote, Building2 } from 'lucide-react';
import Questionnaire from './components/Questionnaire';
import PolicyList from './components/PolicyList';
import PolicyChat from './components/PolicyChat';
import CommunityDiscussion from './components/CommunityDiscussion';
import { UserProfile, Policy } from './types';
import { generatePoliciesFromProfile, apiClient } from './services/api';

function LandingPage() {
  const navigate = useNavigate();

  const handleExploreLaws = () => {
    navigate('/questionnaire');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-2">
              <Building2 className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">ChiUnity</span>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-gray-900 px-4 py-2 text-sm font-medium transition-colors">
                Sign In
              </button>
              <button 
                onClick={handleExploreLaws}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-20 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <Building2 className="h-4 w-4 mr-2" />
              Serving the City of Chicago
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight mb-8">
              Understand Chicago's Laws,
              <span className="text-blue-600"> Engage</span> Your Community
            </h1>
            <p className="text-xl text-gray-600 mb-12 leading-relaxed">
              Navigate Chicago's policies and regulations with confidence. From understanding complex ordinances 
              to taking action in your community - we make civic engagement accessible to every Chicagoan.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <button 
                onClick={handleExploreLaws}
                className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
              >
                <span>Explore Chicago Laws</span>
                <ArrowRight className="h-5 w-5" />
              </button>
            </div>
          </div>

        </div>
      </section>

      {/* Three-Step Process */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              From Confusion to Action in Three Steps
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Understanding Chicago's laws is just the beginning. Once you know what's happening in your city, 
              you can make your voice heard and create real change.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="bg-blue-100 rounded-lg p-3 w-fit mb-6">
                <Search className="h-6 w-6 text-blue-600" />
              </div>
              <div className="flex items-center mb-4">
                <span className="bg-blue-600 text-white text-sm font-bold px-3 py-1 rounded-full mr-3">1</span>
                <h3 className="text-xl font-semibold text-gray-900">Understand</h3>
              </div>
              <p className="text-gray-600 leading-relaxed mb-4">
                Search and discover Chicago policies that affect you. Our AI translates complex legal language into clear, actionable insights.
              </p>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• Zoning regulations</li>
                <li>• Business licensing</li>
                <li>• Housing ordinances</li>
                <li>• Transportation policies</li>
              </ul>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="bg-green-100 rounded-lg p-3 w-fit mb-6">
                <MessageSquare className="h-6 w-6 text-green-600" />
              </div>
              <div className="flex items-center mb-4">
                <span className="bg-green-600 text-white text-sm font-bold px-3 py-1 rounded-full mr-3">2</span>
                <h3 className="text-xl font-semibold text-gray-900">Engage</h3>
              </div>
              <p className="text-gray-600 leading-relaxed mb-4">
                Join community discussions about policies that matter to you. Share perspectives and learn from fellow Chicagoans.
              </p>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• Neighborhood forums</li>
                <li>• Policy discussions</li>
                <li>• Expert insights</li>
                <li>• Community Q&A</li>
              </ul>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="bg-purple-100 rounded-lg p-3 w-fit mb-6">
                <Vote className="h-6 w-6 text-purple-600" />
              </div>
              <div className="flex items-center mb-4">
                <span className="bg-purple-600 text-white text-sm font-bold px-3 py-1 rounded-full mr-3">3</span>
                <h3 className="text-xl font-semibold text-gray-900">Act</h3>
              </div>
              <p className="text-gray-600 leading-relaxed mb-4">
                Take informed action on policies. Support, oppose, or propose changes with the backing of community knowledge.
              </p>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• Contact aldermen</li>
                <li>• Attend city meetings</li>
                <li>• Organize campaigns</li>
                <li>• Track policy changes</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Community Showcase */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Chicago's Civic Community
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Join thousands of engaged Chicagoans who are already making informed decisions and driving positive change in their neighborhoods.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8 border border-gray-100">
              <div className="flex items-center mb-6">
                <Users className="h-8 w-8 text-blue-600 mr-3" />
                <div>
                  <h3 className="text-2xl font-bold text-gray-900">5,200+</h3>
                  <p className="text-gray-600">Active Community Members</p>
                </div>
              </div>
              <p className="text-gray-700">
                From Lincoln Park to Pilsen, Chicagoans across all 77 neighborhoods are using our platform to stay informed and engaged with local governance.
              </p>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-8 border border-gray-100">
              <div className="flex items-center mb-6">
                <MessageSquare className="h-8 w-8 text-green-600 mr-3" />
                <div>
                  <h3 className="text-2xl font-bold text-gray-900">1,800+</h3>
                  <p className="text-gray-600">Policy Discussions</p>
                </div>
              </div>
              <p className="text-gray-700">
                From housing developments to transportation improvements, our community actively discusses the policies shaping Chicago's future.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-blue-600 rounded-2xl p-12 text-center text-white">
            <Building2 className="h-16 w-16 mx-auto mb-8 opacity-80" />
            <h2 className="text-4xl font-bold mb-6">
              Ready to Shape Chicago's Future?
            </h2>
            <p className="text-xl text-blue-100 mb-10 max-w-2xl mx-auto">
              Understanding is power. Join your fellow Chicagoans in making informed decisions about the policies that shape our great city.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={handleExploreLaws}
                className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-medium hover:bg-gray-50 transition-colors"
              >
                Create Free Account
              </button>
              <button 
                onClick={handleExploreLaws}
                className="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-white hover:text-blue-600 transition-colors"
              >
                Explore Chicago Policies
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Building2 className="h-6 w-6" />
              <span className="text-lg font-semibold">ChiUnity</span>
            </div>
            <div className="flex items-center space-x-4">
              <a 
                href="https://forms.google.com/your-lawyer-form" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white text-sm transition-colors"
              >
                I am a lawyer
              </a>
              <p className="text-gray-400">© 2025 ChiUnity. Empowering Chicago's civic engagement.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function App() {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | null>(null);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [hasEngagedWithPolicy, setHasEngagedWithPolicy] = useState(false);

  const handleQuestionnaireComplete = async (profile: UserProfile) => {
    setUserProfile(profile);
    try {
      const generatedPolicies = await generatePoliciesFromProfile(profile, apiClient);
      setPolicies(generatedPolicies);
    } catch (error) {
      console.error('Failed to generate policies:', error);
      // Fallback to empty policies or show error message
      setPolicies([]);
    }
  };

  const handlePolicySelect = (policy: Policy) => {
    setSelectedPolicy(policy);
    setHasEngagedWithPolicy(false);
  };

  const handleBackToPolicies = () => {
    setSelectedPolicy(null);
  };

  const handleTalkAboutIt = () => {
    setHasEngagedWithPolicy(true);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route 
          path="/questionnaire" 
          element={<Questionnaire onComplete={handleQuestionnaireComplete} />} 
        />
        <Route 
          path="/policies" 
          element={
            userProfile ? (
              <PolicyList 
                policies={policies} 
                onPolicySelect={handlePolicySelect} 
              />
            ) : (
              <LandingPage />
            )
          } 
        />
        <Route 
          path="/chat" 
          element={
            selectedPolicy ? (
              <PolicyChat 
                policy={selectedPolicy}
                onBack={handleBackToPolicies}
                onTalkAboutIt={handleTalkAboutIt}
                hasEngaged={hasEngagedWithPolicy}
              />
            ) : (
              <LandingPage />
            )
          } 
        />
        <Route 
          path="/community" 
          element={
            <CommunityDiscussion 
              policyTitle={selectedPolicy?.title} 
            />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;