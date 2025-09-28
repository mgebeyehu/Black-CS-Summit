export interface UserProfile {
  // Personal Demographics
  age: string;
  gender: string;
  maritalStatus: string;
  householdSize: string;
  
  // Citizenship & Residency
  nationality: string;
  immigrationStatus: string;
  residencyStatus: string;
  timeInChicago: string;
  
  // Employment & Income
  employmentStatus: string;
  industry: string;
  incomeLevel: string;
  unionMembership: string;
  
  // Housing & Living Situation
  housingStatus: string;
  leaseOrMortgage: string;
  neighborhood: string;
  landlordOrTenant: string;
  
  // Education & Student Status
  studentStatus: string;
  educationLevel: string;
  schoolType: string;
  
  // Health & Accessibility
  healthInsurance: string;
  disabilityNeeds: string;
  mentalHealthStatus: string;
  
  // Criminal & Legal Background
  criminalRecord: string;
  legalCaseInvolvement: string;
  
  // Transportation & Mobility
  driversLicense: string;
  carOwnership: string;
  publicTransitUser: string;
  
  // Civic & Political
  voterRegistration: string;
  militaryStatus: string;
  
  // Chicago-Specific
  gunOwnership: string;
  cannabisUse: string;
  smallBusinessOwner: string;
  environmentalFactors: string;
  localPrograms: string;
}

export interface Policy {
  id: string;
  title: string;
  description: string;
  category: string;
  relevanceScore: number;
  fullDocument?: {
    document_id: string;
    title: string;
    content: string;
    document_type: string;
    category: string;
    jurisdiction: string;
    authority: string;
    url: string;
    effective_date: string;
    metadata: {
      section_number?: string;
      code_type?: string;
      last_updated?: string;
    };
  };
}

export interface ChatMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export interface DiscussionThread {
  id: string;
  title: string;
  author: string;
  replies: number;
  lastActivity: string;
  category: string;
  policyId?: string;
}