import { UserProfile, Policy } from '../types';

export const generatePoliciesForProfile = (profile: UserProfile): Policy[] => {
  const policies: Policy[] = [];

  // Housing-related policies
  if (profile.housingStatus === 'Renter' || profile.landlordOrTenant === 'Tenant') {
    policies.push({
      id: 'rent-control',
      title: 'Chicago Rent Control Ordinance',
      description: 'Regulations on rent increases and tenant protections in Chicago.',
      category: 'Housing',
      relevanceScore: 0.95
    });
    policies.push({
      id: 'tenant-rights',
      title: 'Residential Landlord Tenant Ordinance (RLTO)',
      description: 'Comprehensive tenant rights and landlord obligations in Chicago.',
      category: 'Housing',
      relevanceScore: 0.9
    });
  }

  if (profile.housingStatus === 'Homeowner') {
    policies.push({
      id: 'property-tax',
      title: 'Property Tax Assessment Appeals',
      description: 'Process for appealing property tax assessments in Cook County.',
      category: 'Housing',
      relevanceScore: 0.85
    });
  }

  // Employment-related policies
  if (profile.employmentStatus !== 'Unemployed' && profile.employmentStatus !== 'Retired') {
    policies.push({
      id: 'minimum-wage',
      title: 'Chicago Minimum Wage Ordinance',
      description: 'Current minimum wage rates and employer obligations.',
      category: 'Employment',
      relevanceScore: 0.8
    });
    policies.push({
      id: 'fair-workweek',
      title: 'Fair Workweek Ordinance',
      description: 'Predictable scheduling requirements for certain industries.',
      category: 'Employment',
      relevanceScore: 0.75
    });
  }

  if (profile.employmentStatus === 'Gig worker') {
    policies.push({
      id: 'gig-worker-rights',
      title: 'App-Based Worker Rights',
      description: 'Protections and benefits for rideshare and delivery workers.',
      category: 'Employment',
      relevanceScore: 0.9
    });
  }

  // Transportation policies
  if (profile.publicTransitUser === 'Daily user' || profile.publicTransitUser === 'Occasional user') {
    policies.push({
      id: 'cta-accessibility',
      title: 'CTA Accessibility Requirements',
      description: 'Public transit accessibility standards and passenger rights.',
      category: 'Transportation',
      relevanceScore: 0.8
    });
  }

  if (profile.carOwnership === 'Own a car') {
    policies.push({
      id: 'parking-regulations',
      title: 'Chicago Parking Regulations',
      description: 'Street parking rules, permits, and violation procedures.',
      category: 'Transportation',
      relevanceScore: 0.85
    });
  }

  // Health-related policies
  if (profile.healthInsurance === 'Uninsured' || profile.healthInsurance === 'Medicaid') {
    policies.push({
      id: 'healthcare-access',
      title: 'Chicago Health Access Programs',
      description: 'Public health programs and community health center access.',
      category: 'Healthcare',
      relevanceScore: 0.9
    });
  }

  // Business-related policies
  if (profile.smallBusinessOwner === 'Small business owner' || profile.smallBusinessOwner === 'Planning to start') {
    policies.push({
      id: 'business-licensing',
      title: 'Chicago Business License Requirements',
      description: 'Licensing requirements and procedures for different business types.',
      category: 'Business',
      relevanceScore: 0.95
    });
    policies.push({
      id: 'small-business-support',
      title: 'Small Business Support Programs',
      description: 'City programs and incentives for small businesses.',
      category: 'Business',
      relevanceScore: 0.85
    });
  }

  // Cannabis-related policies
  if (profile.cannabisUse === 'Recreational user' || profile.cannabisUse === 'Medical user') {
    policies.push({
      id: 'cannabis-regulations',
      title: 'Chicago Cannabis Regulations',
      description: 'Local rules for cannabis use, possession, and dispensary operations.',
      category: 'Cannabis',
      relevanceScore: 0.8
    });
  }

  // Immigration-related policies
  if (profile.immigrationStatus !== 'N/A') {
    policies.push({
      id: 'sanctuary-city',
      title: 'Chicago Sanctuary City Ordinance',
      description: 'Protections for immigrants and limits on federal cooperation.',
      category: 'Immigration',
      relevanceScore: 0.9
    });
  }

  // Student-related policies
  if (profile.studentStatus === 'Current student') {
    policies.push({
      id: 'student-housing',
      title: 'Student Housing Protections',
      description: 'Special protections and regulations for student housing.',
      category: 'Education',
      relevanceScore: 0.8
    });
  }

  // Default policies that affect everyone
  policies.push({
    id: 'municipal-code',
    title: 'Chicago Municipal Code Overview',
    description: 'General city ordinances that affect all residents.',
    category: 'General',
    relevanceScore: 0.6
  });

  return policies.sort((a, b) => b.relevanceScore - a.relevanceScore);
};