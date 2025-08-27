import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { JobApplicationService } from '../services/JobApplicationService';
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

describe('JobApplicationService', () => {
  let jobApplicationService: JobApplicationService;

  beforeEach(() => {
    // Create a new instance of JobApplicationService before each test
    jobApplicationService = new JobApplicationService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('listApplications', () => {
    it('should call apiService.get with correct parameters and return application list', async () => {
      // Arrange
      const status = 'applied';
      const limit = 10;
      const offset = 0;
      const mockResponse = {
        applications: [
          {
            id: 'app123',
            job_id: 'job123',
            user_profile_id: 'user123',
            status: 'applied',
            applied_date: '2023-01-15T10:30:00Z',
            resume_version: 'v1',
            cover_letter: 'I am interested in this position...',
            notes: 'Follow up in one week',
            follow_up_date: '2023-01-22T10:30:00Z',
            interview_scheduled: false,
            created_at: '2023-01-15T10:30:00Z',
            updated_at: '2023-01-15T10:30:00Z',
          }
        ],
        total: 1,
        page: 1,
        page_size: limit,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobApplicationService.listApplications(status, limit, offset);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/applications?status=${status}&limit=${limit}&offset=${offset}`);
      expect(result).toEqual(mockResponse);
    });

    it('should call apiService.get without status parameter when status is not provided', async () => {
      // Arrange
      const limit = 10;
      const offset = 0;
      const mockResponse = {
        applications: [],
        total: 0,
        page: 1,
        page_size: limit,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobApplicationService.listApplications(undefined, limit, offset);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/applications?limit=${limit}&offset=${offset}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getApplication', () => {
    it('should call apiService.get with correct parameters and return application details', async () => {
      // Arrange
      const applicationId = 'app123';
      const mockResponse = {
        id: applicationId,
        job_id: 'job123',
        user_profile_id: 'user123',
        status: 'applied',
        applied_date: '2023-01-15T10:30:00Z',
        resume_version: 'v1',
        cover_letter: 'I am interested in this position...',
        notes: 'Follow up in one week',
        follow_up_date: '2023-01-22T10:30:00Z',
        interview_scheduled: false,
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobApplicationService.getApplication(applicationId);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/applications/${applicationId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createApplication', () => {
    it('should call apiService.post with correct parameters and return application creation response', async () => {
      // Arrange
      const applicationData = {
        user_profile_id: 'user123',
        job_id: 'job123',
        resume_version: 'v1',
        cover_letter: 'I am interested in this position...',
        notes: 'Follow up in one week',
      };
      
      const mockResponse = {
        id: 'app123',
        ...applicationData,
        status: 'applied',
        applied_date: '2023-01-15T10:30:00Z',
        follow_up_date: '2023-01-22T10:30:00Z',
        interview_scheduled: false,
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobApplicationService.createApplication(applicationData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/applications', applicationData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateApplication', () => {
    it('should call apiService.put with correct parameters and return application update response', async () => {
      // Arrange
      const applicationId = 'app123';
      const updateData = {
        status: 'interview_scheduled',
        notes: 'Interview scheduled for next week',
        follow_up_date: '2023-01-29T10:30:00Z',
        interview_scheduled: true,
      };
      
      const mockResponse = {
        id: applicationId,
        job_id: 'job123',
        user_profile_id: 'user123',
        status: 'interview_scheduled',
        applied_date: '2023-01-15T10:30:00Z',
        resume_version: 'v1',
        cover_letter: 'I am interested in this position...',
        notes: 'Interview scheduled for next week',
        follow_up_date: '2023-01-29T10:30:00Z',
        interview_scheduled: true,
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobApplicationService.updateApplication(applicationId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/applications/${applicationId}`, updateData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteApplication', () => {
    it('should call apiService.delete with correct parameters and return application deletion response', async () => {
      // Arrange
      const applicationId = 'app123';
      const mockResponse = {
        message: 'Application deleted successfully'
      };
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await jobApplicationService.deleteApplication(applicationId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/applications/${applicationId}`);
      expect(result).toEqual(mockResponse);
    });
  });
});