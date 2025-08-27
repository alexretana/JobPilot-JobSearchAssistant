import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { SkillBankService } from '../services/SkillBankService';
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
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.createSkillBank(skillBankData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith('/skill-banks', skillBankData);
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
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.getSkillBank(userId);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/skill-banks/${userId}`);
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
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.updateSkillBank(userId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/skill-banks/${userId}`, updateData);
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
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.deleteSkillBank(userId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/skill-banks/${userId}`);
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
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.addSkill(userId, skillData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith(`/skill-banks/${userId}/skills`, skillData);
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
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.updateSkill(userId, skillId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/skill-banks/${userId}/skills/${skillId}`, updateData);
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
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.deleteSkill(userId, skillId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/skill-banks/${userId}/skills/${skillId}`);
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
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.addExperience(userId, experienceData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith(`/skill-banks/${userId}/experiences`, experienceData);
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
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.updateExperience(userId, experienceId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/skill-banks/${userId}/experiences/${experienceId}`, updateData);
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
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await skillBankService.deleteExperience(userId, experienceId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/skill-banks/${userId}/experiences/${experienceId}`);
      expect(result).toEqual(mockResponse);
    });
  });
});