import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { SkillBankService } from '../../src/services/SkillBankService';
import { ApiService } from '../../src/services/ApiService';

// Mock the global fetch function
const mockFetch = vi.fn();

// Set up the global fetch mock before importing anything
global.fetch = mockFetch;

// Import the service after setting up the mock
import { SkillBankService } from '../../src/services/SkillBankService';

describe('SkillBankService', () => {
  let skillBankService: SkillBankService;

  beforeEach(() => {
    // Create a new instance of SkillBankService before each test
    skillBankService = new SkillBankService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('createSkillBank', () => {
    it('should call apiService.post with correct parameters and return skill bank creation response', async () => {
      // Arrange
      const skillBankData = {
        user_id: 'user123',
        initial_skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        default_summary: 'Experienced software developer',
      };
      
      const mockResponse = {
        id: 'skillbank123',
        user_id: 'user123',
        skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.createSkillBank(skillBankData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('/api/skill-banks', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(skillBankData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getSkillBank', () => {
    it('should call apiService.get with correct parameters and return skill bank details', async () => {
      // Arrange
      const userId = 'user123';
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-15T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.getSkillBank(userId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}`, expect.objectContaining({
        method: 'GET',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateSkillBank', () => {
    it('should call apiService.put with correct parameters and return skill bank update response', async () => {
      // Arrange
      const userId = 'user123';
      const updateData = {
        default_summary: 'Senior software developer with 5+ years experience',
      };
      
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        default_summary: 'Senior software developer with 5+ years experience',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.updateSkillBank(userId, updateData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}`, expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(updateData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteSkillBank', () => {
    it('should call apiService.delete with correct parameters and return skill bank deletion response', async () => {
      // Arrange
      const userId = 'user123';
      const mockResponse = {
        message: 'Skill bank archived successfully'
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.deleteSkillBank(userId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}`, expect.objectContaining({
        method: 'DELETE',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('addSkill', () => {
    it('should call apiService.post with correct parameters and return skill addition response', async () => {
      // Arrange
      const userId = 'user123';
      const skillData = {
        name: 'Python',
        level: 'Advanced',
        category: 'Programming Languages',
      };
      
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [
          { name: 'JavaScript', level: 'Intermediate' },
          { name: 'Python', level: 'Advanced', category: 'Programming Languages' },
        ],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.addSkill(userId, skillData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}/skills`, expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(skillData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateSkill', () => {
    it('should call apiService.put with correct parameters and return skill update response', async () => {
      // Arrange
      const userId = 'user123';
      const skillId = 'skill456';
      const updateData = {
        level: 'Expert',
        years_experience: 5,
      };
      
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [
          { 
            id: skillId,
            name: 'Python', 
            level: 'Expert', 
            category: 'Programming Languages',
            years_experience: 5,
          },
        ],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.updateSkill(userId, skillId, updateData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}/skills/${skillId}`, expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(updateData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteSkill', () => {
    it('should call apiService.delete with correct parameters and return skill deletion response', async () => {
      // Arrange
      const userId = 'user123';
      const skillId = 'skill456';
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [
          { name: 'JavaScript', level: 'Intermediate' },
        ],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.deleteSkill(userId, skillId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}/skills/${skillId}`, expect.objectContaining({
        method: 'DELETE',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('addExperience', () => {
    it('should call apiService.post with correct parameters and return experience addition response', async () => {
      // Arrange
      const userId = 'user123';
      const experienceData = {
        company: 'Tech Corp',
        position: 'Software Engineer',
        location: 'San Francisco, CA',
        start_date: '2020-01-01',
        end_date: '2023-01-01',
        is_current: false,
        default_description: 'Developed web applications using modern technologies',
        skills_used: ['JavaScript', 'Python'],
        technologies: ['React', 'Node.js'],
      };
      
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        work_experiences: [experienceData],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.addExperience(userId, experienceData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}/experiences`, expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(experienceData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateExperience', () => {
    it('should call apiService.put with correct parameters and return experience update response', async () => {
      // Arrange
      const userId = 'user123';
      const experienceId = 'exp456';
      const updateData = {
        position: 'Senior Software Engineer',
        end_date: '2023-06-01',
      };
      
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        work_experiences: [
          {
            id: experienceId,
            company: 'Tech Corp',
            position: 'Senior Software Engineer',
            location: 'San Francisco, CA',
            start_date: '2020-01-01',
            end_date: '2023-06-01',
            is_current: false,
            default_description: 'Developed web applications using modern technologies',
            skills_used: ['JavaScript', 'Python'],
            technologies: ['React', 'Node.js'],
          }
        ],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.updateExperience(userId, experienceId, updateData);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}/experiences/${experienceId}`, expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(updateData),
      }));
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteExperience', () => {
    it('should call apiService.delete with correct parameters and return experience deletion response', async () => {
      // Arrange
      const userId = 'user123';
      const experienceId = 'exp456';
      const mockResponse = {
        id: 'skillbank123',
        user_id: userId,
        skills: [{ name: 'JavaScript', level: 'Intermediate' }],
        work_experiences: [],
        default_summary: 'Experienced software developer',
        created_at: '2023-01-15T10:30:00Z',
        updated_at: '2023-01-22T10:30:00Z',
      };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      // Act
      const result = await skillBankService.deleteExperience(userId, experienceId);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(`/api/skill-banks/${userId}/experiences/${experienceId}`, expect.objectContaining({
        method: 'DELETE',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      }));
      expect(result).toEqual(mockResponse);
    });
  });
});