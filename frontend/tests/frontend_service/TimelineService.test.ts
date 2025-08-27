import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { TimelineService } from '../../src/services/TimelineService';
import { ApiService } from '../../src/services/ApiService';

// Mock ApiService
const mockApiService = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
};

vi.mock('../../src/services/ApiService', () => {
  return {
    ApiService: vi.fn(() => mockApiService),
  };
});

describe('TimelineService', () => {
  let timelineService: TimelineService;

  beforeEach(() => {
    // Create a new instance of TimelineService before each test
    timelineService = new TimelineService();
    
    // Clear all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Restore all mocks
    vi.restoreAllMocks();
  });

  describe('getUserTimeline', () => {
    it('should call apiService.get with correct parameters and return user timeline', async () => {
      // Arrange
      const userProfileId = 'user123';
      const options = {
        limit: 10,
        offset: 0,
        job_id: 'job123',
        event_types: ['job_saved', 'application_submitted'],
        days_back: 30,
      };
      
      const mockResponse = [
        {
          id: 'event123',
          user_profile_id: userProfileId,
          event_type: 'job_saved',
          title: 'Saved Job',
          description: 'Saved a job at Tech Corp',
          timestamp: '2023-01-15T10:30:00Z',
          related_job_id: 'job123',
          related_application_id: null,
          metadata: {},
        }
      ];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.getUserTimeline(userProfileId, options);

      // Assert
      expect(mockApiService.get).toHaveBeenCalled();
      const calledWith = mockApiService.get.mock.calls[0][0];
      expect(calledWith).toContain(`/timeline/user/${userProfileId}?`);
      expect(calledWith).toContain('limit=10');
      expect(calledWith).toContain('job_id=job123');
      expect(calledWith).toContain('event_types=job_saved');
      expect(calledWith).toContain('event_types=application_submitted');
      expect(calledWith).toContain('days_back=30');
      expect(result).toEqual(mockResponse);
    });

    it('should call apiService.get with minimal parameters when options are not provided', async () => {
      // Arrange
      const userProfileId = 'user123';
      const mockResponse = [];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.getUserTimeline(userProfileId);

      // Assert
      expect(mockApiService.get).toHaveBeenCalledWith(`/timeline/user/${userProfileId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getUserMilestones', () => {
    it('should call apiService.get with correct parameters and return user milestones', async () => {
      // Arrange
      const userProfileId = 'user123';
      const options = {
        limit: 5,
        days_back: 90,
      };
      
      const mockResponse = [
        {
          id: 'milestone123',
          user_profile_id: userProfileId,
          event_type: 'application_submitted',
          title: 'First Application',
          description: 'Submitted first job application',
          timestamp: '2023-01-15T10:30:00Z',
          related_job_id: 'job123',
          related_application_id: 'app123',
          metadata: {},
        }
      ];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.getUserMilestones(userProfileId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('limit', '5');
      params.set('days_back', '90');
      
      expect(mockApiService.get).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/milestones?${params.toString()}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getUpcomingEvents', () => {
    it('should call apiService.get with correct parameters and return upcoming events', async () => {
      // Arrange
      const userProfileId = 'user123';
      const options = {
        days_ahead: 14,
        limit: 10,
      };
      
      const mockResponse = [
        {
          id: 'event456',
          user_profile_id: userProfileId,
          event_type: 'interview_scheduled',
          title: 'Interview Scheduled',
          description: 'Interview with Tech Corp',
          timestamp: '2023-02-01T10:00:00Z',
          related_job_id: 'job123',
          related_application_id: 'app123',
          metadata: {
            interview_type: 'Technical',
            interviewer: 'John Smith',
          },
        }
      ];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.getUpcomingEvents(userProfileId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('days_ahead', '14');
      params.set('limit', '10');
      
      expect(mockApiService.get).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/upcoming?${params.toString()}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getJobTimeline', () => {
    it('should call apiService.get with correct parameters and return job timeline', async () => {
      // Arrange
      const jobId = 'job123';
      const options = {
        user_profile_id: 'user123',
        limit: 5,
      };
      
      const mockResponse = [
        {
          id: 'event789',
          user_profile_id: 'user123',
          event_type: 'job_saved',
          title: 'Job Saved',
          description: 'Saved job at Tech Corp',
          timestamp: '2023-01-15T10:30:00Z',
          related_job_id: jobId,
          related_application_id: null,
          metadata: {},
        }
      ];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.getJobTimeline(jobId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('user_profile_id', 'user123');
      params.set('limit', '5');
      
      expect(mockApiService.get).toHaveBeenCalledWith(`/timeline/job/${jobId}?${params.toString()}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getApplicationTimeline', () => {
    it('should call apiService.get with correct parameters and return application timeline', async () => {
      // Arrange
      const applicationId = 'app123';
      const options = {
        limit: 10,
      };
      
      const mockResponse = [
        {
          id: 'event101',
          user_profile_id: 'user123',
          event_type: 'application_submitted',
          title: 'Application Submitted',
          description: 'Submitted application for Software Engineer position',
          timestamp: '2023-01-15T10:30:00Z',
          related_job_id: 'job123',
          related_application_id: applicationId,
          metadata: {},
        }
      ];
      
      mockApiService.get.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.getApplicationTimeline(applicationId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('limit', '10');
      
      expect(mockApiService.get).toHaveBeenCalledWith(`/timeline/application/${applicationId}?${params.toString()}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createTimelineEvent', () => {
    it('should call apiService.post with correct parameters and return created timeline event', async () => {
      // Arrange
      const userProfileId = 'user123';
      const eventData = {
        event_type: 'custom_event',
        title: 'Custom Event',
        description: 'This is a custom event',
        timestamp: '2023-01-15T10:30:00Z',
        related_job_id: 'job123',
        related_application_id: 'app123',
        metadata: {
          custom_field: 'custom_value',
        },
      };
      
      const mockResponse = {
        id: 'event202',
        user_profile_id: userProfileId,
        ...eventData,
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.createTimelineEvent(userProfileId, eventData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/event`, eventData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createCustomEvent', () => {
    it('should call apiService.post with correct parameters and return created custom event', async () => {
      // Arrange
      const userProfileId = 'user123';
      const customEventData = {
        title: 'Custom Event',
        description: 'This is a custom event',
        timestamp: '2023-01-15T10:30:00Z',
        metadata: {
          custom_field: 'custom_value',
        },
      };
      
      const mockResponse = {
        id: 'event303',
        user_profile_id: userProfileId,
        event_type: 'custom_event',
        ...customEventData,
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.createCustomEvent(userProfileId, customEventData);

      // Assert
      expect(mockApiService.post).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/custom-event`, customEventData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateTimelineEvent', () => {
    it('should call apiService.put with correct parameters and return updated timeline event', async () => {
      // Arrange
      const eventId = 'event123';
      const updateData = {
        title: 'Updated Event',
        description: 'This is an updated event',
        metadata: {
          updated_field: 'updated_value',
        },
      };
      
      const mockResponse = {
        id: eventId,
        user_profile_id: 'user123',
        event_type: 'job_saved',
        title: 'Updated Event',
        description: 'This is an updated event',
        timestamp: '2023-01-15T10:30:00Z',
        related_job_id: 'job123',
        related_application_id: null,
        metadata: {
          updated_field: 'updated_value',
        },
      };
      
      mockApiService.put.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.updateTimelineEvent(eventId, updateData);

      // Assert
      expect(mockApiService.put).toHaveBeenCalledWith(`/timeline/event/${eventId}`, updateData);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('deleteTimelineEvent', () => {
    it('should call apiService.delete with correct parameters and return deletion response', async () => {
      // Arrange
      const eventId = 'event123';
      const mockResponse = {
        message: 'Timeline event deleted successfully'
      };
      
      mockApiService.delete.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.deleteTimelineEvent(eventId);

      // Assert
      expect(mockApiService.delete).toHaveBeenCalledWith(`/timeline/event/${eventId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('logJobSaved', () => {
    it('should call apiService.post with correct parameters and return logged job saved event', async () => {
      // Arrange
      const userProfileId = 'user123';
      const jobId = 'job123';
      const options = {
        job_title: 'Software Engineer',
        company_name: 'Tech Corp',
        notes: 'Interesting opportunity',
        tags: ['remote', 'javascript'],
      };
      
      const mockResponse = {
        id: 'event404',
        user_profile_id: userProfileId,
        event_type: 'job_saved',
        title: 'Saved Job: Software Engineer at Tech Corp',
        description: 'Saved job posting for Software Engineer at Tech Corp',
        timestamp: '2023-01-15T10:30:00Z',
        related_job_id: jobId,
        related_application_id: null,
        metadata: {
          job_title: 'Software Engineer',
          company_name: 'Tech Corp',
          notes: 'Interesting opportunity',
          tags: ['remote', 'javascript'],
        },
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.logJobSaved(userProfileId, jobId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('job_title', 'Software Engineer');
      params.set('company_name', 'Tech Corp');
      params.set('notes', 'Interesting opportunity');
      params.append('tags', 'remote');
      params.append('tags', 'javascript');
      
      expect(mockApiService.post).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/job/${jobId}/saved?${params.toString()}`, {
        method: 'POST',
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('logApplicationSubmitted', () => {
    it('should call apiService.post with correct parameters and return logged application submitted event', async () => {
      // Arrange
      const userProfileId = 'user123';
      const applicationId = 'app123';
      const options = {
        job_id: 'job123',
        job_title: 'Software Engineer',
        company_name: 'Tech Corp',
        application_method: 'company_website',
      };
      
      const mockResponse = {
        id: 'event505',
        user_profile_id: userProfileId,
        event_type: 'application_submitted',
        title: 'Application Submitted: Software Engineer at Tech Corp',
        description: 'Submitted application for Software Engineer position at Tech Corp via company website',
        timestamp: '2023-01-15T10:30:00Z',
        related_job_id: 'job123',
        related_application_id: applicationId,
        metadata: {
          job_title: 'Software Engineer',
          company_name: 'Tech Corp',
          application_method: 'company_website',
        },
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.logApplicationSubmitted(userProfileId, applicationId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('job_id', 'job123');
      params.set('job_title', 'Software Engineer');
      params.set('company_name', 'Tech Corp');
      params.set('application_method', 'company_website');
      
      expect(mockApiService.post).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/application/${applicationId}/submitted?${params.toString()}`, {
        method: 'POST',
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('logInterviewScheduled', () => {
    it('should call apiService.post with correct parameters and return logged interview scheduled event', async () => {
      // Arrange
      const userProfileId = 'user123';
      const applicationId = 'app123';
      const options = {
        job_id: 'job123',
        job_title: 'Software Engineer',
        company_name: 'Tech Corp',
        interview_date: '2023-02-01T10:00:00Z',
        interview_type: 'Technical',
        interviewer: 'John Smith',
      };
      
      const mockResponse = {
        id: 'event606',
        user_profile_id: userProfileId,
        event_type: 'interview_scheduled',
        title: 'Interview Scheduled: Software Engineer at Tech Corp',
        description: 'Interview scheduled for Software Engineer position at Tech Corp on 2023-02-01',
        timestamp: '2023-01-15T10:30:00Z',
        related_job_id: 'job123',
        related_application_id: applicationId,
        metadata: {
          job_title: 'Software Engineer',
          company_name: 'Tech Corp',
          interview_date: '2023-02-01T10:00:00Z',
          interview_type: 'Technical',
          interviewer: 'John Smith',
        },
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.logInterviewScheduled(userProfileId, applicationId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('job_id', 'job123');
      params.set('job_title', 'Software Engineer');
      params.set('company_name', 'Tech Corp');
      params.set('interview_date', '2023-02-01T10:00:00Z');
      params.set('interview_type', 'Technical');
      params.set('interviewer', 'John Smith');
      
      expect(mockApiService.post).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/application/${applicationId}/interview-scheduled?${params.toString()}`, {
        method: 'POST',
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('logStatusChange', () => {
    it('should call apiService.post with correct parameters and return logged status change event', async () => {
      // Arrange
      const userProfileId = 'user123';
      const applicationId = 'app123';
      const options = {
        job_id: 'job123',
        job_title: 'Software Engineer',
        company_name: 'Tech Corp',
        old_status: 'applied',
        new_status: 'interview_scheduled',
        notes: 'Interview scheduled for next week',
      };
      
      const mockResponse = {
        id: 'event707',
        user_profile_id: userProfileId,
        event_type: 'status_changed',
        title: 'Application Status Changed: Software Engineer at Tech Corp',
        description: 'Application status changed from applied to interview_scheduled',
        timestamp: '2023-01-15T10:30:00Z',
        related_job_id: 'job123',
        related_application_id: applicationId,
        metadata: {
          job_title: 'Software Engineer',
          company_name: 'Tech Corp',
          old_status: 'applied',
          new_status: 'interview_scheduled',
          notes: 'Interview scheduled for next week',
        },
      };
      
      mockApiService.post.mockResolvedValueOnce(mockResponse);

      // Act
      const result = await timelineService.logStatusChange(userProfileId, applicationId, options);

      // Assert
      const params = new URLSearchParams();
      params.set('job_id', 'job123');
      params.set('job_title', 'Software Engineer');
      params.set('company_name', 'Tech Corp');
      params.set('old_status', 'applied');
      params.set('new_status', 'interview_scheduled');
      params.set('notes', 'Interview scheduled for next week');
      
      expect(mockApiService.post).toHaveBeenCalledWith(`/timeline/user/${userProfileId}/application/${applicationId}/status-changed?${params.toString()}`, {
        method: 'POST',
      });
      expect(result).toEqual(mockResponse);
    });
  });
});