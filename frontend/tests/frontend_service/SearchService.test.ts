import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { SearchService } from '../../src/services/SearchService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { SearchService } from '../../src/services/SearchService';

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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await searchService.semanticSearch(query, limit);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/search/semantic?query=${query}&limit=${limit}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await searchService.semanticSearch(query);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/search/semantic?query=${query}&limit=20`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await searchService.hybridSearch(query, limit);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/search/hybrid?query=${query}&limit=${limit}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await searchService.hybridSearch(query);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/search/hybrid?query=${query}&limit=20`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });
});