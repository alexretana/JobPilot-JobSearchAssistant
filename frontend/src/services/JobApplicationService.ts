// frontend/src/services/JobApplicationService.ts
import { apiService } from './ApiService';

// Define types for job applications
export interface JobApplication {
  id: string;
  job_id: string;
  user_profile_id: string;
  status: string;
  applied_date?: string;
  response_date?: string;
  resume_version?: string;
  cover_letter?: string;
  notes?: string;
  follow_up_date?: string;
  interview_scheduled?: boolean;
  created_at: string;
  updated_at: string;
}

export interface JobApplicationCreate {
  user_profile_id: string;
  job_id: string;
  resume_version?: string;
  cover_letter?: string;
  notes?: string;
}

export interface JobApplicationUpdate {
  status?: string;
  response_date?: string;
  resume_version?: string;
  cover_letter?: string;
  notes?: string;
  follow_up_date?: string;
  interview_scheduled?: boolean;
}

export interface JobApplicationListResponse {
  applications: JobApplication[];
  total: number;
  page: number;
  page_size: number;
}

export interface JobApplicationResponse extends JobApplication {}

export class JobApplicationService {
  private apiService = apiService;

  async listApplications(filters: JobApplicationFilters): Promise<JobApplicationListResponse> {
    const params = new URLSearchParams();
    
    if (status) {
      params.append('status', status);
    }
    
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    
    return this.apiService.get<JobApplicationListResponse>(`/applications?${params.toString()}`);
  }

  async getApplication(applicationId: string): Promise<JobApplicationResponse> {
    return this.apiService.get<JobApplicationResponse>(`/applications/${applicationId}`);
  }

  async createApplication(applicationData: JobApplicationCreate): Promise<JobApplicationResponse> {
    return this.apiService.post<JobApplicationResponse>('/applications', applicationData);
  }

  async updateApplication(
    applicationId: string,
    updateData: JobApplicationUpdate
  ): Promise<JobApplicationResponse> {
    return this.apiService.put<JobApplicationResponse>(`/applications/${applicationId}`, updateData);
  }

  async deleteApplication(applicationId: string): Promise<{ message: string }> {
    return this.apiService.delete<{ message: string }>(`/applications/${applicationId}`);
  }
}