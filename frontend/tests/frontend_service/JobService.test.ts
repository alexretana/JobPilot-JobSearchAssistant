import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { JobService } from '../../src/services/JobService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { JobService } from '../../src/services/JobService';

describe('JobService', () => {
  let jobService: JobService;

  beforeEach(() => {
    // Create a new instance of JobService before each test
    jobService = new JobService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('searchJobs', () => {
    it('should call apiService.get with correct parameters and return job search results', async () => {
      // Arrange
      const filters = {
        query: 'software engineer',
        job_type: 'Full-time',
        remote_type: 'Remote',
        experience_level: 'Mid-level',
        salary_min: 100000,
        salary_max: 150000,
        location: 'San Francisco, CA',
        company: 'Tech Corp',
        posted_after: '2023-01-01',
        posted_before: '2023-12-31'
      };
      
      const mockResponse = {
        message: 'Job search results',
        user_id: 'user123',
        filters_applied: filters,
        results: [
          {
            job_id: 'job123',
            title: 'Software Engineer',
            company: 'Tech Corp',
            location: 'San Francisco, CA',
            job_type: 'Full-time',
            remote_type: 'Remote',
            experience_level: 'Mid-level',
            salary_min: 100000,
            salary_max: 150000,
            posted_date: '2023-01-15T10:30:00Z',
          }
        ],
        total_results: 1,
        page: 1,
        page_size: 20,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.searchJobs(filters);

      // Assert
      // Build query string
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });
      
      expect(mockFetch).toHaveBeenCalledWith(`/api/jobs/search?${params.toString()}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getJobStatistics', () => {
    it('should call apiService.get with correct parameters and return job statistics', async () => {
      // Arrange
      const mockResponse = {
        message: 'Job statistics',
        user_id: 'user123',
        total_jobs: 1250,
        jobs_by_type: { 'Full-time': 850, 'Part-time': 120, 'Contract': 280 },
        jobs_by_remote_type: { 'Remote': 450, 'Hybrid': 520, 'On-site': 280 },
        jobs_by_experience_level: {
          'Entry-level': 300,
          'Mid-level': 600,
          'Senior-level': 350,
        },
        average_salary_by_type: {
          'Full-time': { min: 95000, max: 165000 },
          'Part-time': { min: 45000, max: 85000 },
          'Contract': { min: 75000, max: 145000 },
        },
        top_locations: [
          { location: 'San Francisco, CA', count: 180 },
          { location: 'New York, NY', count: 150 },
          { location: 'Remote', count: 140 },
        ],
        top_companies: [
          { company: 'Tech Corp', count: 45 },
          { company: 'Innovate Inc', count: 38 },
          { company: 'Digital Solutions', count: 32 },
        ],
        recent_trend: { last_7_days: 85, last_30_days: 320, last_90_days: 750 },
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.getJobStatistics();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/jobs/statistics', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('listJobs', () => {
    it('should call apiService.get with correct parameters and return job list', async () => {
      // Arrange
      const mockResponse = {
        message: 'List all jobs',
        user_id: 'user123'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.listJobs();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/jobs', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getJob', () => {
    it('should call apiService.get with correct parameters and return job details', async () => {
      // Arrange
      const jobId = 'job123';
      const mockResponse = {
        job_id: jobId,
        title: 'Software Engineer',
        user_id: 'user123'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.getJob(jobId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/jobs/${jobId}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createJob', () => {
    it('should call apiService.post with correct parameters and return job creation response', async () => {
      // Arrange
      const mockResponse = {
        message: 'Job created',
        user_id: 'user123'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.createJob();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/jobs', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateJob', () => {
    it('should call apiService.put with correct parameters and return job update response', async () => {
      // Arrange
      const jobId = 'job123';
      const mockResponse = {
        message: `Job ${jobId} updated`,
        user_id: 'user123'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.updateJob(jobId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/jobs/${jobId}`, expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteJob', () => {
    it('should call apiService.delete with correct parameters and return job deletion response', async () => {
      // Arrange
      const jobId = 'job123';
      const mockResponse = {
        message: `Job ${jobId} deleted`,
        user_id: 'user123'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await jobService.deleteJob(jobId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/jobs/${jobId}`, expect.objectContaining({
        method: 'DELETE',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('formatSalary', () => {
    it('should format salary correctly when both min and max are provided', () => {
      // Act
      const result = jobService.formatSalary(100000, 150000);

      // Assert
      expect(result).toBe('$100,000 - $150,000');
    });

    it('should format salary correctly when only min is provided', () => {
      // Act
      const result = jobService.formatSalary(100000, undefined);

      // Assert
      expect(result).toBe('$100,000+');
    });

    it('should format salary correctly when only max is provided', () => {
      // Act
      const result = jobService.formatSalary(undefined, 150000);

      // Assert
      expect(result).toBe('Up to $150,000');
    });

    it('should return "Salary not specified" when neither min nor max is provided', () => {
      // Act
      const result = jobService.formatSalary(undefined, undefined);

      // Assert
      expect(result).toBe('Salary not specified');
    });
  });

  describe('formatPostedDate', () => {
    it('should return "Date not specified" when posted date is null', () => {
      // Act
      const result = jobService.formatPostedDate(null);

      // Assert
      expect(result).toBe('Date not specified');
    });

    it('should return "1 day ago" when job was posted yesterday', () => {
      // Arrange
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const postedDate = yesterday.toISOString();

      // Act
      const result = jobService.formatPostedDate(postedDate);

      // Assert
      expect(result).toBe('1 day ago');
    });

    it('should return "X days ago" when job was posted less than 7 days ago', () => {
      // Arrange
      const fiveDaysAgo = new Date();
      fiveDaysAgo.setDate(fiveDaysAgo.getDate() - 5);
      const postedDate = fiveDaysAgo.toISOString();

      // Act
      const result = jobService.formatPostedDate(postedDate);

      // Assert
      expect(result).toBe('5 days ago');
    });

    it('should return "X weeks ago" when job was posted less than 30 days ago', () => {
      // Arrange
      const threeWeeksAgo = new Date();
      threeWeeksAgo.setDate(threeWeeksAgo.getDate() - 21);
      const postedDate = threeWeeksAgo.toISOString();

      // Act
      const result = jobService.formatPostedDate(postedDate);

      // Assert
      expect(result).toBe('3 weeks ago');
    });

    it('should return formatted date when job was posted more than 30 days ago', () => {
      // Arrange
      const oldDate = new Date('2022-01-01');
      const postedDate = oldDate.toISOString();

      // Act
      const result = jobService.formatPostedDate(postedDate);

      // Assert
      expect(result).toBe(oldDate.toLocaleDateString());
    });
  });

  describe('getJobTypeLabel', () => {
    it('should return "Not specified" when job type is null', () => {
      // Act
      const result = jobService.getJobTypeLabel(null);

      // Assert
      expect(result).toBe('Not specified');
    });

    it('should return correct label for known job types', () => {
      // Act
      const result = jobService.getJobTypeLabel('Full-time');

      // Assert
      expect(result).toBe('Full-time');
    });

    it('should return the job type itself when not in the predefined labels', () => {
      // Act
      const result = jobService.getJobTypeLabel('Freelance');

      // Assert
      expect(result).toBe('Freelance');
    });
  });

  describe('getRemoteTypeLabel', () => {
    it('should return "Not specified" when remote type is null', () => {
      // Act
      const result = jobService.getRemoteTypeLabel(null);

      // Assert
      expect(result).toBe('Not specified');
    });

    it('should return correct label for known remote types', () => {
      // Act
      const result = jobService.getRemoteTypeLabel('Remote');

      // Assert
      expect(result).toBe('Remote');
    });

    it('should return the remote type itself when not in the predefined labels', () => {
      // Act
      const result = jobService.getRemoteTypeLabel('Hybrid');

      // Assert
      expect(result).toBe('Hybrid');
    });
  });

  describe('getRemoteTypeIcon', () => {
    it('should return correct icon for known remote types', () => {
      // Act
      const result = jobService.getRemoteTypeIcon('Remote');

      // Assert
      expect(result).toBe('🏠');
    });

    it('should return default icon for unknown remote types', () => {
      // Act
      const result = jobService.getRemoteTypeIcon('Unknown');

      // Assert
      expect(result).toBe('📍');
    });

    it('should return default icon when remote type is null', () => {
      // Act
      const result = jobService.getRemoteTypeIcon(null);

      // Assert
      expect(result).toBe('📍');
    });
  });
});