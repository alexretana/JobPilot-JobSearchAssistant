// frontend/src/services/TimelineService.ts
import { ApiService } from './ApiService';

// Define types for timeline events
export type TimelineEventType =
  | 'job_saved'
  | 'application_submitted'
  | 'interview_scheduled'
  | 'status_changed'
  | 'custom_event'
  | string;

export interface TimelineEvent {
  id: string;
  user_profile_id: string;
  event_type: TimelineEventType;
  title: string;
  description: string;
  timestamp: string;
  related_job_id?: string;
  related_application_id?: string;
  metadata: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface CreateTimelineEventRequest {
  event_type: TimelineEventType;
  title: string;
  description: string;
  timestamp: string;
  related_job_id?: string;
  related_application_id?: string;
  metadata?: Record<string, any>;
}

export interface CreateCustomEventRequest {
  title: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface UpdateTimelineEventRequest {
  title?: string;
  description?: string;
  timestamp?: string;
  metadata?: Record<string, any>;
}

export class TimelineService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async getUserTimeline(
    userProfileId: string,
    options?: {
      limit?: number;
      offset?: number;
      job_id?: string;
      event_types?: TimelineEventType[];
      days_back?: number;
    }
  ): Promise<TimelineEvent[]> {
    const params = new URLSearchParams();

    if (options?.limit) params.set('limit', options.limit.toString());
    if (options?.offset) params.set('offset', options.offset.toString());
    if (options?.job_id) params.set('job_id', options.job_id);
    if (options?.days_back) params.set('days_back', options.days_back.toString());
    if (options?.event_types) {
      options.event_types.forEach(type => params.append('event_types', type));
    }

    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiService.get<TimelineEvent[]>(`/timeline/user/${userProfileId}${queryString}`);
  }

  async getUserMilestones(
    userProfileId: string,
    options?: {
      limit?: number;
      days_back?: number;
    }
  ): Promise<TimelineEvent[]> {
    const params = new URLSearchParams();

    if (options?.limit) params.set('limit', options.limit.toString());
    if (options?.days_back) params.set('days_back', options.days_back.toString());

    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiService.get<TimelineEvent[]>(`/timeline/user/${userProfileId}/milestones${queryString}`);
  }

  async getUpcomingEvents(
    userProfileId: string,
    options?: {
      days_ahead?: number;
      limit?: number;
    }
  ): Promise<TimelineEvent[]> {
    const params = new URLSearchParams();

    if (options?.days_ahead) params.set('days_ahead', options.days_ahead.toString());
    if (options?.limit) params.set('limit', options.limit.toString());

    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiService.get<TimelineEvent[]>(`/timeline/user/${userProfileId}/upcoming${queryString}`);
  }

  async getJobTimeline(
    jobId: string,
    options?: {
      user_profile_id?: string;
      limit?: number;
    }
  ): Promise<TimelineEvent[]> {
    const params = new URLSearchParams();

    if (options?.user_profile_id) params.set('user_profile_id', options.user_profile_id);
    if (options?.limit) params.set('limit', options.limit.toString());

    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiService.get<TimelineEvent[]>(`/timeline/job/${jobId}${queryString}`);
  }

  async getApplicationTimeline(
    applicationId: string,
    options?: {
      limit?: number;
    }
  ): Promise<TimelineEvent[]> {
    const params = new URLSearchParams();

    if (options?.limit) params.set('limit', options.limit.toString());

    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiService.get<TimelineEvent[]>(`/timeline/application/${applicationId}${queryString}`);
  }

  async createTimelineEvent(
    userProfileId: string,
    request: CreateTimelineEventRequest
  ): Promise<TimelineEvent> {
    return this.apiService.post<TimelineEvent>(`/timeline/user/${userProfileId}/event`, request);
  }

  async createCustomEvent(
    userProfileId: string,
    request: CreateCustomEventRequest
  ): Promise<TimelineEvent> {
    return this.apiService.post<TimelineEvent>(`/timeline/user/${userProfileId}/custom-event`, request);
  }

  async updateTimelineEvent(
    eventId: string,
    request: UpdateTimelineEventRequest
  ): Promise<TimelineEvent> {
    return this.apiService.put<TimelineEvent>(`/timeline/event/${eventId}`, request);
  }

  async deleteTimelineEvent(eventId: string): Promise<{ message: string }> {
    return this.apiService.delete<{ message: string }>(`/timeline/event/${eventId}`);
  }

  async logJobSaved(
    userProfileId: string,
    jobId: string,
    options: {
      job_title: string;
      company_name: string;
      notes?: string;
      tags?: string[];
    }
  ): Promise<TimelineEvent> {
    const params = new URLSearchParams();
    params.set('job_title', options.job_title);
    params.set('company_name', options.company_name);
    if (options.notes) params.set('notes', options.notes);
    if (options.tags) {
      options.tags.forEach(tag => params.append('tags', tag));
    }

    return this.apiService.post<TimelineEvent>(
      `/timeline/user/${userProfileId}/job/${jobId}/saved?${params.toString()}`,
      {
        method: 'POST',
      }
    );
  }

  async logApplicationSubmitted(
    userProfileId: string,
    applicationId: string,
    options: {
      job_id: string;
      job_title: string;
      company_name: string;
      application_method?: string;
    }
  ): Promise<TimelineEvent> {
    const params = new URLSearchParams();
    params.set('job_id', options.job_id);
    params.set('job_title', options.job_title);
    params.set('company_name', options.company_name);
    if (options.application_method) params.set('application_method', options.application_method);

    return this.apiService.post<TimelineEvent>(
      `/timeline/user/${userProfileId}/application/${applicationId}/submitted?${params.toString()}`,
      {
        method: 'POST',
      }
    );
  }

  async logInterviewScheduled(
    userProfileId: string,
    applicationId: string,
    options: {
      job_id: string;
      job_title: string;
      company_name: string;
      interview_date: string;
      interview_type?: string;
      interviewer?: string;
    }
  ): Promise<TimelineEvent> {
    const params = new URLSearchParams();
    params.set('job_id', options.job_id);
    params.set('job_title', options.job_title);
    params.set('company_name', options.company_name);
    params.set('interview_date', options.interview_date);
    if (options.interview_type) params.set('interview_type', options.interview_type);
    if (options.interviewer) params.set('interviewer', options.interviewer);

    return this.apiService.post<TimelineEvent>(
      `/timeline/user/${userProfileId}/application/${applicationId}/interview-scheduled?${params.toString()}`,
      {
        method: 'POST',
      }
    );
  }

  async logStatusChange(
    userProfileId: string,
    applicationId: string,
    options: {
      job_id: string;
      job_title: string;
      company_name: string;
      old_status: string;
      new_status: string;
      notes?: string;
    }
  ): Promise<TimelineEvent> {
    const params = new URLSearchParams();
    params.set('job_id', options.job_id);
    params.set('job_title', options.job_title);
    params.set('company_name', options.company_name);
    params.set('old_status', options.old_status);
    params.set('new_status', options.new_status);
    if (options.notes) params.set('notes', options.notes);

    return this.apiService.post<TimelineEvent>(
      `/timeline/user/${userProfileId}/application/${applicationId}/status-changed?${params.toString()}`,
      {
        method: 'POST',
      }
    );
  }
}