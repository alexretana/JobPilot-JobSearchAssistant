import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AnalyticsService } from '../../src/services/AnalyticsService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { AnalyticsService } from '../../src/services/AnalyticsService';

describe('AnalyticsService', () => {
  let analyticsService: AnalyticsService;

  beforeEach(() => {
    // Create a new instance of AnalyticsService before each test
    analyticsService = new AnalyticsService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('getGeneralStats', () => {
    it('should call apiService.get with correct parameters and return general statistics', async () => {
      // Arrange
      const mockResponse = {
        total_users: 1000,
        total_jobs: 5000,
        total_applications: 2500,
        total_companies: 500,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getGeneralStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/general', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getJobStats', () => {
    it('should call apiService.get with correct parameters and return job statistics', async () => {
      // Arrange
      const mockResponse = {
        total_jobs: 5000,
        jobs_by_type: {
          'Full-time': 3000,
          'Part-time': 1000,
          'Contract': 1000,
        },
        jobs_by_remote_type: {
          'Remote': 2000,
          'Hybrid': 1500,
          'On-site': 1500,
        },
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getJobStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/jobs', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getUserStats', () => {
    it('should call apiService.get with correct parameters and return user statistics', async () => {
      // Arrange
      const mockResponse = {
        total_users: 1000,
        users_by_role: {
          'job_seeker': 800,
          'recruiter': 200,
        },
        users_by_status: {
          'active': 900,
          'inactive': 100,
        },
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getUserStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/users', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getApplicationStats', () => {
    it('should call apiService.get with correct parameters and return application statistics', async () => {
      // Arrange
      const mockResponse = {
        total_applications: 2500,
        applications_by_status: {
          'applied': 1500,
          'interview_scheduled': 700,
          'rejected': 300,
        },
        applications_by_type: {
          'online': 2000,
          'referral': 500,
        },
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getApplicationStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/applications', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getResumeStats', () => {
    it('should call apiService.get with correct parameters and return resume statistics', async () => {
      // Arrange
      const mockResponse = {
        total_resumes: 1200,
        resumes_by_type: {
          'professional': 800,
          'student': 300,
          'executive': 100,
        },
        resumes_by_status: {
          'active': 1000,
          'archived': 200,
        },
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getResumeStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/resumes', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getSkillBankStats', () => {
    it('should call apiService.get with correct parameters and return skill bank statistics', async () => {
      // Arrange
      const mockResponse = {
        total_skill_banks: 900,
        avg_skills_per_bank: 15.5,
        most_common_skills: [
          { skill: 'JavaScript', count: 500 },
          { skill: 'Python', count: 450 },
          { skill: 'Java', count: 400 },
        ],
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getSkillBankStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/skill-banks', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getJobSourceStats', () => {
    it('should call apiService.get with correct parameters and return job source statistics', async () => {
      // Arrange
      const mockResponse = {
        total_job_sources: 20,
        active_sources: 15,
        jobs_by_source: [
          { source: 'LinkedIn', job_count: 2000 },
          { source: 'Indeed', job_count: 1500 },
          { source: 'Company Website', job_count: 1500 },
        ],
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await analyticsService.getJobSourceStats();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/stats/job-sources', expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });
});