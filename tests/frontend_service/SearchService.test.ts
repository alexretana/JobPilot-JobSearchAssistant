import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { SearchService } from '../services/SearchService';
import { ApiService } from '../services/ApiService';

// Mock ApiService
const mockApiService = {
  get: vi.fn(),
};

vi.mock('../services/ApiService', () => {
  return {
    ApiService: vi.fn().mockImplementation(() => mockApiService),
  };
});

describe('SearchService', () => {
  let searchService: SearchService;

  beforeEach(() => {
    // Create a new instance of SearchService before each test
    searchService = new SearchService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('semanticSearch', () => {
    it('should call apiService.get with correct parameters and return semantic search results', async () => {
      // Arrange
      const query = 'software engineer';
      const limit = 10;
      const mockResponse = {
        query: query,
        results: [
          {
            job_id: 'job123',
            title: 'Software Engineer',
            company: 'Tech Corp',
            similarity_score: 0.95,
          }
        ],
        total_results: 1,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await searchService.semanticSearch(query, limit);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/search/semantic?query=${query}&limit=${limit}`);
      expect(result).toEqual(mockResponse);
    });

    it('should call apiService.get with default limit when limit is not provided', async () => {
      // Arrange
      const query = 'software engineer';
      const mockResponse = {
        query: query,
        results: [],
        total_results: 0,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await searchService.semanticSearch(query);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/search/semantic?query=${query}&limit=20`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('hybridSearch', () => {
    it('should call apiService.get with correct parameters and return hybrid search results', async () => {
      // Arrange
      const query = 'software engineer';
      const limit = 10;
      const mockResponse = {
        query: query,
        results: [
          {
            job_id: 'job123',
            title: 'Software Engineer',
            company: 'Tech Corp',
            keyword_score: 0.85,
            semantic_score: 0.95,
            combined_score: 0.90,
          }
        ],
        total_results: 1,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await searchService.hybridSearch(query, limit);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/search/hybrid?query=${query}&limit=${limit}`);
      expect(result).toEqual(mockResponse);
    });

    it('should call apiService.get with default limit when limit is not provided', async () => {
      // Arrange
      const query = 'software engineer';
      const mockResponse = {
        query: query,
        results: [],
        total_results: 0,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await searchService.hybridSearch(query);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/search/hybrid?query=${query}&limit=20`);
      expect(result).toEqual(mockResponse);
    });
  });
});