import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ResumeService } from '../../src/services/ResumeService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { ResumeService } from '../../src/services/ResumeService';

describe('ResumeService', () => {
  let resumeService: ResumeService;

  beforeEach(() => {
    // Create a new instance of ResumeService before each test
    resumeService = new ResumeService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('listResumes', () => {
    it('should call apiService.get with correct parameters and return resume list', async () => {
      // Arrange
      const status = 'active';
      const limit = 10;
      const offset = 0;
      const mockResponse = {
        resumes: [
          {
            id: 'resume123',
            user_id: 'user123',
            title: 'Software Engineer Resume',
            status: 'active',
            resume_type: 'professional',
            created_at: '2023-01-15T10:30:00Z',
            updated_at: '2023-01-15T10:30:00Z',
            version: 1,
          }
        ],
        total: 1,
        page: 1,
        page_size: limit,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await resumeService.listResumes(status, limit, offset);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/resumes?status=${status}&limit=${limit}&offset=${offset}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });

    it('should call apiService.get without status parameter when status is not provided', async () => {
      // Arrange
      const limit = 10;
      const offset = 0;
      const mockResponse = {
        resumes: [],
        total: 0,
        page: 1,
        page_size: limit,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await resumeService.listResumes(undefined, limit, offset);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/resumes?limit=${limit}&offset=${offset}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getResume', () => {
    it('should call apiService.get with correct parameters and return resume details', async () => {
      // Arrange
      const resumeId = 'resume123';
      const mockResponse = {
        id: resumeId,
        user_id: 'user123',
        title: 'Software Engineer Resume',
        status: 'active',
        resume_type: 'professional',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
        version: 1,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await resumeService.getResume(resumeId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/resumes/${resumeId}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createResume', () => {
    it('should call apiService.post with correct parameters and return resume creation response', async () => {
      // Arrange
      const resumeData = {
        user_id: 'user123',
        title: 'New Resume',
        resume_type: 'professional',
        contact_info: {
          full_name: 'John Doe',
          email: 'john.doe@example.com',
        },
      };
      
      const mockResponse = {
        id: 'resume456',
        ...resumeData,
        status: 'draft',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
        version: 1,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await resumeService.createResume(resumeData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/resumes', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(resumeData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateResume', () => {
    it('should call apiService.put with correct parameters and return resume update response', async () => {
      // Arrange
      const resumeId = 'resume123';
      const updateData = {
        title: 'Updated Resume',
        status: 'active',
      };
      
      const mockResponse = {
        id: resumeId,
        user_id: 'user123',
        title: 'Updated Resume',
        status: 'active',
        resume_type: 'professional',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
        version: 2,
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await resumeService.updateResume(resumeId, updateData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/resumes/${resumeId}`, expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(updateData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteResume', () => {
    it('should call apiService.delete with correct parameters and return resume deletion response', async () => {
      // Arrange
      const resumeId = 'resume123';
      const mockResponse = {
        message: 'Resume deleted successfully'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await resumeService.deleteResume(resumeId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/resumes/${resumeId}`, expect.objectContaining({
        method: 'DELETE',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });
});