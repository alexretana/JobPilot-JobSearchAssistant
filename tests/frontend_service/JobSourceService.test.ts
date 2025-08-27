import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { JobSourceService } from '../services/JobSourceService';
import { ApiService } from '../services/ApiService';

// Mock ApiService
const mockApiService = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
};

vi.mock('../services/ApiService', () => {
  return {
    ApiService: vi.fn().mockImplementation(() => mockApiService),
  };
});

describe('JobSourceService', () => {
  let jobSourceService: JobSourceService;

  beforeEach(() => {
    // Create a new instance of JobSourceService before each test
    jobSourceService = new JobSourceService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('listJobSources', () => {
    it('should call apiService.get with correct parameters and return job source list', async () => {
      // Arrange
      const mockResponse = {
        job_sources: [
          {
            id: 'source123',
            name: 'LinkedIn',
            url: 'https://linkedin.com',
            description: 'Professional networking platform',
            is_active: true,
            last_scraped: '2023-01-15T10:30:00Z',
            created_at: '2023-01-01T10:30:00Z',
            updated_at: '2023-01-15T10:30:00Z',
          }
        ],
        total: 1,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobSourceService.listJobSources();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/job-sources');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getJobSource', () => {
    it('should call apiService.get with correct parameters and return job source details', async () => {
      // Arrange
      const sourceId = 'source123';
      const mockResponse = {
        id: sourceId,
        name: 'LinkedIn',
        url: 'https://linkedin.com',
        description: 'Professional networking platform',
        is_active: true,
        last_scraped: '2023-01-15T10:30:00Z',
        created_at: '2023-01-01T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobSourceService.getJobSource(sourceId);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/job-sources/${sourceId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createJobSource', () => {
    it('should call apiService.post with correct parameters and return job source creation response', async () => {
      // Arrange
      const jobSourceData = {
        name: 'Indeed',
        url: 'https://indeed.com',
        description: 'Job search engine',
        is_active: true,
      };
      
      const mockResponse = {
        id: 'source456',
        ...jobSourceData,
        last_scraped: null,
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobSourceService.createJobSource(jobSourceData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/job-sources', jobSourceData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateJobSource', () => {
    it('should call apiService.put with correct parameters and return job source update response', async () => {
      // Arrange
      const sourceId = 'source123';
      const updateData = {
        name: 'LinkedIn Jobs',
        description: 'Professional networking platform and job board',
        is_active: true,
      };
      
      const mockResponse = {
        id: sourceId,
        name: 'LinkedIn Jobs',
        url: 'https://linkedin.com',
        description: 'Professional networking platform and job board',
        is_active: true,
        last_scraped: '2023-01-15T10:30:00Z',
        created_at: '2023-01-01T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobSourceService.updateJobSource(sourceId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/job-sources/${sourceId}`, updateData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteJobSource', () => {
    it('should call apiService.delete with correct parameters and return job source deletion response', async () => {
      // Arrange
      const sourceId = 'source123';
      const mockResponse = {
        message: 'Job source deleted successfully'
      };
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobSourceService.deleteJobSource(sourceId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/job-sources/${sourceId}`);
      expect(result).toEqual(mockResponse);
    });
  });
});