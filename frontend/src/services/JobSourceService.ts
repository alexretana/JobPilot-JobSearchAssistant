// frontend/src/services/JobSourceService.ts
import { ApiService } from './ApiService';

// Define types for job sources
export interface JobSource {
  id: string;
  name: string;
  url: string;
  description?: string;
  is_active: boolean;
  last_scraped?: string;
  created_at: string;
  updated_at: string;
}

export interface JobSourceCreate {
  name: string;
  url: string;
  description?: string;
  is_active: boolean;
}

export interface JobSourceUpdate {
  name?: string;
  url?: string;
  description?: string;
  is_active?: boolean;
}

export interface JobSourceListResponse {
  job_sources: JobSource[];
  total: number;
}

export interface JobSourceResponse extends JobSource {}

export class JobSourceService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async listJobSources(): Promise<JobSourceListResponse> {
    return this.apiService.get<JobSourceListResponse>('/job-sources');
  }

  async getJobSource(sourceId: string): Promise<JobSourceResponse> {
    return this.apiService.get<JobSourceResponse>(`/job-sources/${sourceId}`);
  }

  async createJobSource(jobSourceData: JobSourceCreate): Promise<JobSourceResponse> {
    return this.apiService.post<JobSourceResponse>('/job-sources', jobSourceData);
  }

  async updateJobSource(sourceId: string, updateData: JobSourceUpdate): Promise<JobSourceResponse> {
    return this.apiService.put<JobSourceResponse>(`/job-sources/${sourceId}`, updateData);
  }

  async deleteJobSource(sourceId: string): Promise<{ message: string }> {
    return this.apiService.delete<{ message: string }>(`/job-sources/${sourceId}`);
  }
}