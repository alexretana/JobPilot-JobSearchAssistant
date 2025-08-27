import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { UserProfileService } from '../services/UserProfileService';
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

describe('UserProfileService', () => {
  let userProfileService: UserProfileService;

  beforeEach(() => {
    // Create a new instance of UserProfileService before each test
    userProfileService = new UserProfileService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('createProfile', () => {
    it('should call apiService.post with correct parameters and return user profile data', async () => {
      // Arrange
      const profileData = { 
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        preferred_job_types: ['Full-time'],
        preferred_remote_types: ['Remote']
      };
      
      const mockResponse = { 
        id: '1',
        ...profileData,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z'
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await userProfileService.createProfile(profileData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/users', profileData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getProfile', () => {
    it('should call apiService.get with correct parameters and return user profile data', async () => {
      // Arrange
      const userId = '1';
      const mockResponse = { 
        id: userId,
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        preferred_job_types: ['Full-time'],
        preferred_remote_types: ['Remote'],
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z'
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await userProfileService.getProfile(userId);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/users/${userId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getDefaultProfile', () => {
    it('should call apiService.get with correct parameters and return default user profile data', async () => {
      // Arrange
      const mockResponse = { 
        id: 'default',
        first_name: 'Default',
        last_name: 'User',
        email: 'default@example.com',
        preferred_job_types: ['Full-time'],
        preferred_remote_types: ['Remote'],
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z'
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await userProfileService.getDefaultProfile();

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith('/users/default');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateProfile', () => {
    it('should call apiService.put with correct parameters and return updated user profile data', async () => {
      // Arrange
      const userId = '1';
      const updateData = { 
        first_name: 'Jane',
        last_name: 'Smith'
      };
      
      const mockResponse = { 
        id: userId,
        first_name: 'Jane',
        last_name: 'Smith',
        email: 'john.doe@example.com',
        preferred_job_types: ['Full-time'],
        preferred_remote_types: ['Remote'],
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-02T00:00:00Z'
      };
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await userProfileService.updateProfile(userId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/users/${userId}`, updateData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteProfile', () => {
    it('should call apiService.delete with correct parameters', async () => {
      // Arrange
      const userId = '1';
      mockApiService.delete.mockResolvedValueOnce({ message: 'User profile deleted successfully' });

      // Act
      const result = await userProfileService.deleteProfile(userId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/users/${userId}`);
      expect(result).toEqual({ message: 'User profile deleted successfully' });
    });
  });

  describe('listProfiles', () => {
    it('should call apiService.get with correct parameters and return paginated user profiles', async () => {
      // Arrange
      const limit = 10;
      const offset = 0;
      const mockResponse = [
        { 
          id: '1',
          first_name: 'John',
          last_name: 'Doe',
          email: 'john.doe@example.com',
          preferred_job_types: ['Full-time'],
          preferred_remote_types: ['Remote'],
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z'
        }
      ];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await userProfileService.listProfiles(limit, offset);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/users?limit=${limit}&offset=${offset}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('searchProfileByEmail', () => {
    it('should call apiService.get with correct parameters and return user profile data', async () => {
      // Arrange
      const email = 'john.doe@example.com';
      const mockResponse = { 
        id: '1',
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        preferred_job_types: ['Full-time'],
        preferred_remote_types: ['Remote'],
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z'
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await userProfileService.searchProfileByEmail(email);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/users/search/by-email?email=${encodeURIComponent(email)}`);
      expect(result).toEqual(mockResponse);
    });
  });
});