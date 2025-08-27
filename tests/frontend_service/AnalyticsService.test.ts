import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AnalyticsService } from '../services/AnalyticsService';
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getGeneralStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/general');
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getJobStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/jobs');
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getUserStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/users');
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getApplicationStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/applications');
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getResumeStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/resumes');
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getSkillBankStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/skill-banks');
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await analyticsService.getJobSourceStats();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/stats/job-sources');
      expect(result).toEqual(mockResponse);
    });
  });
});