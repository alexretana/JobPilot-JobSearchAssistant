import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ApiService } from '../services/ApiService';

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('ApiService', () => {
  let apiService: ApiService;

  beforeEach(() => {
    apiService = new ApiService();
    mockFetch.mockClear();
  });

  afterEach(() => {
    // Clear all mocks
    vi.restoreAllMocks();
  });

  describe('get', () => {
    it('should make a GET request with correct URL and headers', async () => {
      // Arrange
      const mockResponse = { data: 'test' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await apiService.get('/test-endpoint');

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/test-endpoint', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error when the response is not ok', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      });

      // Act & Assert
      await expect(apiService.get('/test-endpoint')).rejects.toThrow('API Error: 404 Not Found');
    });
  });

  describe('post', () => {
    it('should make a POST request with correct URL, headers, and body', async () => {
      // Arrange
      const mockData = { name: 'test' };
      const mockResponse = { id: 1, ...mockData };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await apiService.post('/test-endpoint', mockData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/test-endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(mockData),
      });
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error when the response is not ok', async () => {
      // Arrange
      const mockData = { name: 'test' };
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
      });

      // Act & Assert
      await expect(apiService.post('/test-endpoint', mockData)).rejects.toThrow('API Error: 500 Internal Server Error');
    });
  });

  describe('put', () => {
    it('should make a PUT request with correct URL, headers, and body', async () => {
      // Arrange
      const mockData = { id: 1, name: 'updated test' };
      const mockResponse = mockData;
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await apiService.put('/test-endpoint/1', mockData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/test-endpoint/1', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(mockData),
      });
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error when the response is not ok', async () => {
      // Arrange
      const mockData = { id: 1, name: 'updated test' };
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
      });

      // Act & Assert
      await expect(apiService.put('/test-endpoint/1', mockData)).rejects.toThrow('API Error: 400 Bad Request');
    });
  });

  describe('delete', () => {
    it('should make a DELETE request with correct URL and headers', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ message: 'Deleted successfully' }),
      });

      // Act
      const result = await apiService.delete('/test-endpoint/1');

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/test-endpoint/1', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      expect(result).toEqual({ message: 'Deleted successfully' });
    });

    it('should throw an error when the response is not ok', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 403,
        statusText: 'Forbidden',
      });

      // Act & Assert
      await expect(apiService.delete('/test-endpoint/1')).rejects.toThrow('API Error: 403 Forbidden');
    });
  });
});