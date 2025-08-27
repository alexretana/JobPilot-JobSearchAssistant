import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { JobDeduplicationService } from '../../src/services/JobDeduplicationService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { JobDeduplicationService } from '../../src/services/JobDeduplicationService';

describe('JobDeduplicationService', () => {
  let jobDeduplicationService: JobDeduplicationService;

  beforeEach(() => {
    // Create a new instance of JobDeduplicationService before each test
    jobDeduplicationService = new JobDeduplicationService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('deduplicateJob', () => {
    it('should call apiService.post with correct parameters and return deduplication result', async () => {
      // Arrange
      const jobData = {
        title: 'Software Engineer',
        company: 'Tech Corp',
        description: 'Develop web applications using modern technologies',
      };
      
      const mockResponse = {
        is_duplicate: true,
        duplicate_of: 'job123',
        similarity_score: 0.95,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobDeduplicationService.deduplicateJob(jobData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/job-deduplication/deduplicate', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(jobData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deduplicateBatch', () => {
    it('should call apiService.post with correct parameters and return batch deduplication result', async () => {
      // Arrange
      const jobs = [
        {
          id: 'job123',
          title: 'Software Engineer',
          company: 'Tech Corp',
          description: 'Develop web applications using modern technologies',
        },
        {
          id: 'job456',
          title: 'Software Developer',
          company: 'Tech Corp',
          description: 'Build web applications',
        }
      ];
      
      const mockResponse = {
        duplicates_found: 1,
        duplicate_pairs: [
          {
            job_id_1: 'job123',
            job_id_2: 'job456',
            similarity_score: 0.85,
          }
        ],
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobDeduplicationService.deduplicateBatch(jobs);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/job-deduplication/deduplicate-batch', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({ jobs }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });
});