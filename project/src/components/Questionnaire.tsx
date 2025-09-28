import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ArrowLeft, User, Globe, Briefcase, Home, GraduationCap, Heart, Shield, Car, Vote, Lightbulb } from 'lucide-react';
import { UserProfile } from '../types';

interface QuestionnaireProps {
  onComplete: (profile: UserProfile) => void;
}

const Questionnaire: React.FC<QuestionnaireProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [profile, setProfile] = useState<Partial<UserProfile>>({});
  const navigate = useNavigate();

  const steps = [
    {
      title: "Personal Demographics",
      icon: User,
      questions: [
        { key: 'age', label: 'Age Range', options: ['Under 18', '18-25', '26-35', '36-50', '51-65', '65+'] },
        { key: 'gender', label: 'Gender Identity', options: ['Male', 'Female', 'Non-binary', 'Prefer not to say', 'Other'] },
        { key: 'maritalStatus', label: 'Marital/Family Status', options: ['Single', 'Married', 'Divorced', 'Single parent', 'Caregiver'] },
        { key: 'householdSize', label: 'Household Size', options: ['1 person', '2 people', '3-4 people', '5+ people'] }
      ]
    },
    {
      title: "Citizenship & Residency",
      icon: Globe,
      questions: [
        { key: 'nationality', label: 'Citizenship Status', options: ['US Citizen', 'Permanent Resident', 'Visa Holder', 'Other'] },
        { key: 'immigrationStatus', label: 'Immigration Status', options: ['N/A', 'Student Visa', 'Work Visa', 'Green Card', 'Undocumented'] },
        { key: 'residencyStatus', label: 'Residency Status', options: ['Permanent Chicago resident', 'Temporary resident', 'Moving in', 'Moving out'] },
        { key: 'timeInChicago', label: 'Time in Chicago', options: ['Less than 1 year', '1-3 years', '3-10 years', '10+ years', 'Born here'] }
      ]
    },
    {
      title: "Employment & Income",
      icon: Briefcase,
      questions: [
        { key: 'employmentStatus', label: 'Employment Status', options: ['Full-time', 'Part-time', 'Gig worker', 'Unemployed', 'Self-employed', 'Retired'] },
        { key: 'industry', label: 'Industry/Job Type', options: ['Healthcare', 'Education', 'Technology', 'Service industry', 'Manufacturing', 'Government', 'Other'] },
        { key: 'incomeLevel', label: 'Household Income', options: ['Under $25k', '$25k-$50k', '$50k-$75k', '$75k-$100k', '$100k+'] },
        { key: 'unionMembership', label: 'Union Membership', options: ['Yes', 'No', 'Not applicable'] }
      ]
    },
    {
      title: "Housing & Living",
      icon: Home,
      questions: [
        { key: 'housingStatus', label: 'Housing Status', options: ['Renter', 'Homeowner', 'Unhoused', 'Public housing', 'Living with family'] },
        { key: 'leaseOrMortgage', label: 'Lease vs Mortgage', options: ['Lease/Rent', 'Mortgage', 'Neither', 'Both'] },
        { key: 'neighborhood', label: 'Chicago Neighborhood', options: ['North Side', 'South Side', 'West Side', 'Downtown/Loop', 'Suburbs', 'Other'] },
        { key: 'landlordOrTenant', label: 'Property Role', options: ['Tenant', 'Landlord', 'Homeowner', 'Other'] }
      ]
    },
    {
      title: "Education & Student Status",
      icon: GraduationCap,
      questions: [
        { key: 'studentStatus', label: 'Student Status', options: ['Current student', 'Recent graduate', 'Not a student'] },
        { key: 'educationLevel', label: 'Education Level', options: ['High school', 'Some college', 'Bachelor\'s degree', 'Graduate degree', 'Trade school'] },
        { key: 'schoolType', label: 'School Type', options: ['Public school', 'Private school', 'Community college', 'University', 'N/A'] }
      ]
    },
    {
      title: "Health & Accessibility",
      icon: Heart,
      questions: [
        { key: 'healthInsurance', label: 'Health Insurance', options: ['Medicare', 'Medicaid', 'Private insurance', 'Uninsured', 'Other'] },
        { key: 'disabilityNeeds', label: 'Accessibility Needs', options: ['Yes', 'No', 'Prefer not to say'] },
        { key: 'mentalHealthStatus', label: 'Mental Health Support', options: ['Currently receiving support', 'Need support', 'No support needed', 'Prefer not to say'] }
      ]
    },
    {
      title: "Legal Background",
      icon: Shield,
      questions: [
        { key: 'criminalRecord', label: 'Criminal Record', options: ['Yes', 'No', 'Prefer not to say'] },
        { key: 'legalCaseInvolvement', label: 'Current Legal Cases', options: ['Tenant dispute', 'Employment case', 'Immigration case', 'None', 'Other'] }
      ]
    },
    {
      title: "Transportation",
      icon: Car,
      questions: [
        { key: 'driversLicense', label: 'Driver\'s License', options: ['Valid IL license', 'Out-of-state license', 'No license', 'REAL ID'] },
        { key: 'carOwnership', label: 'Car Ownership', options: ['Own a car', 'Don\'t own a car', 'Shared vehicle'] },
        { key: 'publicTransitUser', label: 'Public Transit Use', options: ['Daily user', 'Occasional user', 'Rarely use', 'Never use'] }
      ]
    },
    {
      title: "Civic & Political",
      icon: Vote,
      questions: [
        { key: 'voterRegistration', label: 'Voter Registration', options: ['Registered in Chicago', 'Registered elsewhere', 'Not registered', 'Not eligible'] },
        { key: 'militaryStatus', label: 'Military Status', options: ['Active military', 'Veteran', 'Military family', 'None'] }
      ]
    },
    {
      title: "Chicago-Specific",
      icon: Lightbulb,
      questions: [
        { key: 'gunOwnership', label: 'Firearm Status', options: ['FOID card holder', 'Interested in FOID', 'Not applicable'] },
        { key: 'cannabisUse', label: 'Cannabis Interest', options: ['Recreational user', 'Medical user', 'Not interested', 'Prefer not to say'] },
        { key: 'smallBusinessOwner', label: 'Business Ownership', options: ['Small business owner', 'Planning to start', 'Employee', 'Not applicable'] },
        { key: 'localPrograms', label: 'Local Program Interest', options: ['Housing assistance', 'Energy programs', 'Tax rebates', 'None', 'All of the above'] }
      ]
    }
  ];

  const handleAnswer = (key: string, value: string) => {
    setProfile(prev => ({ ...prev, [key]: value }));
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete(profile as UserProfile);
      navigate('/policies');
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const currentStepData = steps[currentStep];
  const Icon = currentStepData.icon;
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Step {currentStep + 1} of {steps.length}</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
          <div className="flex items-center mb-6">
            <div className="bg-blue-100 rounded-lg p-3 mr-4">
              <Icon className="h-6 w-6 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">{currentStepData.title}</h2>
          </div>

          <div className="space-y-6">
            {currentStepData.questions.map((question) => (
              <div key={question.key}>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  {question.label}
                </label>
                <div className="grid grid-cols-1 gap-2">
                  {question.options.map((option) => (
                    <button
                      key={option}
                      onClick={() => handleAnswer(question.key, option)}
                      className={`text-left p-3 rounded-lg border transition-colors ${
                        profile[question.key as keyof UserProfile] === option
                          ? 'border-blue-500 bg-blue-50 text-blue-700'
                          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Navigation */}
          <div className="flex justify-between mt-8 pt-6 border-t border-gray-100">
            <button
              onClick={prevStep}
              disabled={currentStep === 0}
              className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Previous
            </button>
            <button
              onClick={nextStep}
              className="flex items-center px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              {currentStep === steps.length - 1 ? 'Complete' : 'Next'}
              <ArrowRight className="h-4 w-4 ml-2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Questionnaire;