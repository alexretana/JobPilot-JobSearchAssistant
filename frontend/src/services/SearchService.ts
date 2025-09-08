// frontend/src/services/SearchService.ts
import { apiService } from './ApiService';

// Define types for search results
export interface SemanticSearchResult {
  job_id: string;
  title: string;
  company: string;
  similarity_score: number;
}

export interface SemanticSearchResponse {
  query: string;
  results: SemanticSearchResult[];
  total_results: number;
}

export interface HybridSearchResult {
  job_id: string;
  title: string;
  company: string;
  keyword_score: number;
  semantic_score: number;
  combined_score: number;
}

export interface HybridSearchResponse {
  query: string;
  results: HybridSearchResult[];
  total_results: number;
}

export class SearchService {
  private apiService = apiService;

  async semanticSearch(query: string, limit: number = 20): Promise<SemanticSearchResponse> {
    return this.apiService.get<SemanticSearchResponse>(`/search/semantic?query=${query}&limit=${limit}`);
  }

  async hybridSearch(query: string, limit: number = 20): Promise<HybridSearchResponse> {
    return this.apiService.get<HybridSearchResponse>(`/search/hybrid?query=${query}&limit=${limit}`);
  }
}