import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AuthService } from '../services/AuthService';
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

describe('AuthService', () => {
  let authService: AuthService;

  beforeEach(() => {
    // Create a new instance of AuthService before each test
    authService = new AuthService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('login', () => {
    it('should call apiService.post with correct parameters and return user data', async () => {
      // Arrange
      const credentials = { email: 'test@example.com', password: 'password123' };
      const mockResponse = { 
        user: { id: '1', email: 'test@example.com' }, 
        access_token: 'token123', 
        token_type: 'bearer' 
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await authService.login(credentials);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/auth/login', credentials);
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error when login fails', async () => {
      // Arrange
      const credentials = { email: 'test@example.com', password: 'wrongpassword' };
      const mockError = new Error('Invalid credentials');
      
      mockApiService.post.mockRejectedValueOnce(mockError);

      // Act & Assert
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
      expect(mockApiService.post).toHaveBeenCalledWith('/auth/login', credentials);
    });
  });

  describe('register', () => {
    it('should call apiService.post with correct parameters and return user data', async () => {
      // Arrange
      const userData = { 
        email: 'newuser@example.com', 
        password: 'password123',
        first_name: 'New',
        last_name: 'User'
      };
      const mockResponse = { 
        user: { id: '2', email: 'newuser@example.com', first_name: 'New', last_name: 'User' }
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await authService.register(userData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/auth/register', userData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('logout', () => {
    it('should call apiService.post with correct parameters', async () => {
      // Arrange
      mockApiService.post.mockResolvedValueOnce({ message: 'Logged out successfully' });

      // Act
      const result = await authService.logout();

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/auth/logout', {});
      expect(result).toEqual({ message: 'Logged out successfully' });
    });
  });

  describe('refreshToken', () => {
    it('should call apiService.post with correct parameters and return new token', async () => {
      // Arrange
      const mockResponse = { 
        access_token: 'newtoken123', 
        token_type: 'bearer' 
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await authService.refreshToken();

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/auth/refresh', {});
      expect(result).toEqual(mockResponse);
    });
  });
});