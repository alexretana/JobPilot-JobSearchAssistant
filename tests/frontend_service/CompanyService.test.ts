import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { CompanyService } from '../services/CompanyService';
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

describe('CompanyService', () => {
  let companyService: CompanyService;

  beforeEach(() => {
    // Create a new instance of CompanyService before each test
    companyService = new CompanyService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('listCompanies', () => {
    it('should call apiService.get with correct parameters and return company list', async () => {
      // Arrange
      const limit = 20;
      const offset = 0;
      const mockResponse = {
        message: 'List all companies',
        user_id: 'user123',
        companies: [
          {
            id: 'company123',
            name: 'Tech Corp',
            industry: 'Technology',
            website: 'https://techcorp.com',
            logo_url: 'https://techcorp.com/logo.png',
            description: 'A leading technology company',
          }
        ],
        total: 1,
        page: 1,
        page_size: limit,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.listCompanies(limit, offset);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/companies?limit=${limit}&offset=${offset}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('searchCompanies', () => {
    it('should call apiService.get with correct parameters and return company search results', async () => {
      // Arrange
      const query = 'tech';
      const mockResponse = {
        message: 'Search companies',
        user_id: 'user123',
        query: query,
        companies: [
          {
            id: 'company123',
            name: 'Tech Corp',
            industry: 'Technology',
            website: 'https://techcorp.com',
            logo_url: 'https://techcorp.com/logo.png',
            description: 'A leading technology company',
          }
        ],
        total: 1,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.searchCompanies(query);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/companies/search?query=${query}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getCompany', () => {
    it('should call apiService.get with correct parameters and return company details', async () => {
      // Arrange
      const companyId = 'company123';
      const mockResponse = {
        id: companyId,
        name: 'Tech Corp',
        industry: 'Technology',
        website: 'https://techcorp.com',
        logo_url: 'https://techcorp.com/logo.png',
        description: 'A leading technology company',
        user_id: 'user123'
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.getCompany(companyId);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/companies/${companyId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createCompany', () => {
    it('should call apiService.post with correct parameters and return company creation response', async () => {
      // Arrange
      const companyData = {
        name: 'New Corp',
        industry: 'Technology',
        website: 'https://newcorp.com',
        description: 'A new technology company',
      };
      
      const mockResponse = {
        message: 'Company created',
        user_id: 'user123',
        company: {
          id: 'newcompany123',
          ...companyData,
        }
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.createCompany(companyData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/companies', companyData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateCompany', () => {
    it('should call apiService.put with correct parameters and return company update response', async () => {
      // Arrange
      const companyId = 'company123';
      const updateData = {
        name: 'Updated Corp',
        industry: 'Technology',
        website: 'https://updatedcorp.com',
        description: 'An updated technology company',
      };
      
      const mockResponse = {
        message: `Company ${companyId} updated`,
        user_id: 'user123',
        company: {
          id: companyId,
          ...updateData,
        }
      };
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.updateCompany(companyId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/companies/${companyId}`, updateData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteCompany', () => {
    it('should call apiService.delete with correct parameters and return company deletion response', async () => {
      // Arrange
      const companyId = 'company123';
      const mockResponse = {
        message: `Company ${companyId} deleted`,
        user_id: 'user123'
      };
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.deleteCompany(companyId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/companies/${companyId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getCompanyJobs', () => {
    it('should call apiService.get with correct parameters and return company jobs', async () => {
      // Arrange
      const companyId = 'company123';
      const limit = 10;
      const offset = 0;
      const mockResponse = {
        message: 'Get jobs for company',
        user_id: 'user123',
        company_id: companyId,
        jobs: [
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
        total: 1,
        page: 1,
        page_size: limit,
      };
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await companyService.getCompanyJobs(companyId, limit, offset);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/companies/${companyId}/jobs?limit=${limit}&offset=${offset}`);
      expect(result).toEqual(mockResponse);
    });
  });
});