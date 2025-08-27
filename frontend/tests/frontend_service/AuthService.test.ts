import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AuthService } from '../../src/services/AuthService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { AuthService } from '../../src/services/AuthService';

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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await authService.login(credentials);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error when login fails', async () => {
      // Arrange
      const credentials = { email: 'test@example.com', password: 'wrongpassword' };
      
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        json: () => Promise.resolve({ detail: 'Invalid credentials' }),
      });

      // Act & Assert
      await expect(authService.login(credentials)).rejects.toThrow('API Error: 401 Unauthorized');
      expect(mockFetch).toHaveBeenCalledWith('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await authService.register(userData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('logout', () => {
    it('should call apiService.post with correct parameters', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ message: 'Logged out successfully' }),
      });

      // Act
      const result = await authService.logout();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/auth/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });
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
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await authService.refreshToken();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });
      expect(result).toEqual(mockResponse);
    });
  });
});