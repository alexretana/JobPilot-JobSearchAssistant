import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { JobDeduplicationService } from '../services/JobDeduplicationService';
import { ApiService } from '../services/ApiService';

// Mock ApiService
const mockApiService = {
  post: vi.fn(),
};

vi.mock('../services/ApiService', () => {
  return {
    ApiService: vi.fn().mockImplementation(() => mockApiService),
  };
});

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
        description: 'Develop web applications',
      };
      
      const mockResponse = {
        is_duplicate: true,
        duplicate_of: 'job123',
        similarity_score: 0.95,
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobDeduplicationService.deduplicateJob(jobData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/job-deduplication/deduplicate', jobData);
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
          description: 'Develop web applications',
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
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobDeduplicationService.deduplicateBatch(jobs);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/job-deduplication/deduplicate-batch', { jobs });
      expect(result).toEqual(mockResponse);
    });
  });
});