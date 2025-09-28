/**
 * API Client for Chicago Legal Document Democratization Platform
 * Handles all communication with the FastAPI backend
 */

export interface BackendDocument {
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
}

export interface SearchRequest {
  query: string;
  jurisdiction?: string;
  category?: string;
  limit?: number;
}

export interface SearchResponse {
  query: string;
  jurisdiction: string;
  category_filter?: string;
  total_results: number;
  results: BackendDocument[];
  search_metadata: {
    search_timestamp: string;
    total_documents_searched: number;
    search_algorithm: string;
  };
}

export interface ChatRequest {
  user_message: string;
  use_context?: boolean;
  max_context_docs?: number;
}

export interface ChatResponse {
  answer: string;
  sources: Array<{
    title: string;
    authority: string;
    url: string;
    category: string;
    similarity_score: number;
    match_reasons: string[];
  }>;
  confidence_score: number;
  jurisdiction: string;
  model: string;
  context_used: number;
  total_documents_searched: number;
  search_metadata: {
    query_processed: string;
    documents_found: number;
    search_timestamp: string;
  };
}

export interface DocumentStats {
  jurisdiction: string;
  data_source: string;
  total_documents: number;
  categories: Record<string, number>;
  authorities: string[];
  date_range: {
    earliest: string;
    latest: string;
  };
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API request failed: ${response.status} ${errorText}`);
    }

    return response.json();
  }

  // Health check
  async getHealth(): Promise<any> {
    return this.request('/health');
  }

  // Get document statistics
  async getDocumentStats(): Promise<DocumentStats> {
    return this.request('/api/v1/documents/stats/legislation');
  }

  // Get all documents
  async getAllDocuments(limit?: number, category?: string): Promise<{
    documents: BackendDocument[];
    total_returned: number;
    filters_applied: { category?: string; authority?: string };
    timestamp: string;
  }> {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    if (category) params.append('category', category);
    
    const queryString = params.toString();
    const endpoint = `/api/v1/documents/${queryString ? `?${queryString}` : ''}`;
    
    return this.request(endpoint);
  }

  // Semantic search
  async semanticSearch(request: SearchRequest): Promise<SearchResponse> {
    return this.request('/api/v1/search/semantic', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Chat with AI
  async chatWithAI(request: ChatRequest): Promise<ChatResponse> {
    return this.request('/api/v1/chat/ask', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Get search suggestions
  async getSearchSuggestions(): Promise<{
    suggestions: string[];
    jurisdiction: string;
  }> {
    return this.request('/api/v1/search/suggestions');
  }

  // Get analytics
  async getAnalytics(): Promise<{
    total_documents: number;
    total_chat_sessions: number;
    category_breakdown: Record<string, number>;
    source_breakdown: Record<string, number>;
    legislation_types: Record<string, number>;
    date_range: {
      earliest: string;
      latest: string;
    };
    system_health: {
      data_freshness: string;
      api_status: string;
      search_performance: string;
    };
  }> {
    return this.request('/api/v1/analytics');
  }

  // Get chat history
  async getChatHistory(limit: number = 10): Promise<{
    chat_history: Array<{
      role: string;
      message: string;
      timestamp: string;
    }>;
    total_messages: number;
  }> {
    return this.request(`/api/v1/chat/history?limit=${limit}`);
  }

  // Clear chat history
  async clearChatHistory(): Promise<{ message: string; timestamp: string }> {
    return this.request('/api/v1/chat/clear', {
      method: 'POST',
    });
  }
}

// Create and export a singleton instance
export const apiClient = new ApiClient();

// Helper function to convert backend documents to frontend policies
export const convertDocumentToPolicy = (doc: BackendDocument, relevanceScore: number = 0.8) => ({
  id: doc.document_id,
  title: doc.title,
  description: doc.content.substring(0, 200) + '...',
  category: doc.category,
  relevanceScore,
  // Include full document data for detailed view
  fullDocument: doc,
});

// Helper function to generate policies based on user profile
export const generatePoliciesFromProfile = async (
  profile: any,
  apiClient: ApiClient
): Promise<any[]> => {
  try {
    // Create search queries based on user profile
    const searchQueries = generateSearchQueriesFromProfile(profile);
    
    // Perform searches and collect results by category
    const policiesByCategory: { [key: string]: any[] } = {
      'construction': [],
      'general': [], // Business items are in general category
      'transportation': [],
      'governance': []
    };
    
    for (const query of searchQueries) {
      try {
        const searchResponse = await apiClient.semanticSearch({
          query: query.query,
          category: query.category,
          limit: 5, // Get more results per query
        });
        
        const policies = searchResponse.results.map((doc, index) => 
          convertDocumentToPolicy(doc, 0.9 - (index * 0.1))
        );
        
        // Group policies by category
        const category = query.category || 'general';
        if (policiesByCategory[category]) {
          policiesByCategory[category].push(...policies);
        }
      } catch (error) {
        console.warn(`Search failed for query: ${query.query}`, error);
      }
    }
    
    // Ensure we have at least 5 policies from each category
    const finalPolicies: any[] = [];
    const targetPerCategory = 5;
    
    for (const [category, policies] of Object.entries(policiesByCategory)) {
      // Remove duplicates within category
      const uniquePolicies = policies.filter((policy, index, self) => 
        index === self.findIndex(p => p.id === policy.id)
      );
      
      // Take up to targetPerCategory policies from this category
      const selectedPolicies = uniquePolicies
        .sort((a, b) => b.relevanceScore - a.relevanceScore)
        .slice(0, targetPerCategory);
      
      finalPolicies.push(...selectedPolicies);
    }
    
    // Sort all policies by relevance score
    return finalPolicies.sort((a, b) => b.relevanceScore - a.relevanceScore);
  } catch (error) {
    console.error('Failed to generate policies from profile:', error);
    return [];
  }
};

// Helper function to generate search queries from user profile
const generateSearchQueriesFromProfile = (profile: any): Array<{query: string, category?: string}> => {
  const queries: Array<{query: string, category?: string}> = [];
  
  // Always include queries for each category to ensure diversity
  queries.push({ query: 'zoning permit construction building', category: 'construction' });
  queries.push({ query: 'sign permit advertisement business', category: 'general' }); // Business items are in general category
  queries.push({ query: 'parking transportation traffic', category: 'transportation' });
  queries.push({ query: 'city council governance ordinance', category: 'governance' });
  queries.push({ query: 'damage claim vehicle pothole', category: 'general' });
  
  // Housing-related queries
  if (profile.housingStatus === 'Renter' || profile.landlordOrTenant === 'Tenant') {
    queries.push({ query: 'tenant rights rent control housing', category: 'construction' });
    queries.push({ query: 'landlord tenant ordinance', category: 'construction' });
  }
  
  if (profile.housingStatus === 'Homeowner') {
    queries.push({ query: 'property tax assessment homeowner', category: 'construction' });
  }
  
  // Employment-related queries
  if (profile.employmentStatus !== 'Unemployed' && profile.employmentStatus !== 'Retired') {
    queries.push({ query: 'minimum wage employment', category: 'business' });
    queries.push({ query: 'fair workweek scheduling', category: 'business' });
  }
  
  if (profile.employmentStatus === 'Gig worker') {
    queries.push({ query: 'gig worker rideshare delivery', category: 'business' });
  }
  
  // Transportation queries
  if (profile.publicTransitUser === 'Daily user' || profile.publicTransitUser === 'Occasional user') {
    queries.push({ query: 'CTA public transit accessibility', category: 'transportation' });
  }
  
  if (profile.carOwnership === 'Own a car') {
    queries.push({ query: 'parking regulations vehicle', category: 'transportation' });
  }
  
  // Health queries
  if (profile.healthInsurance === 'Uninsured' || profile.healthInsurance === 'Medicaid') {
    queries.push({ query: 'healthcare access public health', category: 'governance' });
  }
  
  // Business queries
  if (profile.smallBusinessOwner === 'Small business owner' || profile.smallBusinessOwner === 'Planning to start') {
    queries.push({ query: 'business license requirements', category: 'business' });
    queries.push({ query: 'small business support programs', category: 'business' });
  }
  
  // Cannabis queries
  if (profile.cannabisUse === 'Recreational user' || profile.cannabisUse === 'Medical user') {
    queries.push({ query: 'cannabis marijuana regulations', category: 'governance' });
  }
  
  // Immigration queries
  if (profile.immigrationStatus !== 'N/A') {
    queries.push({ query: 'sanctuary city immigration', category: 'governance' });
  }
  
  // Student queries
  if (profile.studentStatus === 'Current student') {
    queries.push({ query: 'student housing education', category: 'construction' });
  }
  
  // Additional category-specific queries to ensure diversity
  queries.push({ query: 'handicapped parking permit', category: 'transportation' });
  queries.push({ query: 'congratulations recognition service', category: 'governance' });
  queries.push({ query: 'damage claim vehicle', category: 'general' });
  queries.push({ query: 'zoning reclassification', category: 'construction' });
  queries.push({ query: 'sign permit signboard', category: 'general' });
  
  return queries;
};
