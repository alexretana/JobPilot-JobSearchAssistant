// frontend/src/services/AnalyticsService.ts
import { apiService } from './ApiService';

// Define types for analytics data
export interface GeneralStatsResponse {
  total_users: number;
  total_jobs: number;
  total_applications: number;
  total_companies: number;
}

export interface JobStatsResponse {
  total_jobs: number;
  jobs_by_type: Record<string, number>;
  jobs_by_remote_type: Record<string, number>;
}

export interface UserStatsResponse {
  total_users: number;
  users_by_role: Record<string, number>;
  users_by_status: Record<string, number>;
}

export interface ApplicationStatsResponse {
  total_applications: number;
  applications_by_status: Record<string, number>;
  applications_by_type: Record<string, number>;
}

export interface ResumeStatsResponse {
  total_resumes: number;
  resumes_by_type: Record<string, number>;
  resumes_by_status: Record<string, number>;
}

export interface SkillBankStatsResponse {
  total_skill_banks: number;
  avg_skills_per_bank: number;
  most_common_skills: Array<{ skill: string; count: number }>;
}

export interface JobSourceStatsResponse {
  total_job_sources: number;
  active_sources: number;
  jobs_by_source: Array<{ source: string; job_count: number }>;
}

export class AnalyticsService {
  private apiService = apiService;

  async getGeneralStats(): Promise<GeneralStatsResponse> {
    return this.apiService.get<GeneralStatsResponse>('/stats/general');
  }

  async getJobStats(): Promise<JobStatsResponse> {
    return this.apiService.get<JobStatsResponse>('/stats/jobs');
  }

  async getUserStats(): Promise<UserStatsResponse> {
    return this.apiService.get<UserStatsResponse>('/stats/users');
  }

  async getApplicationStats(): Promise<ApplicationStatsResponse> {
    return this.apiService.get<ApplicationStatsResponse>('/stats/applications');
  }

  async getResumeStats(): Promise<ResumeStatsResponse> {
    return this.apiService.get<ResumeStatsResponse>('/stats/resumes');
  }

  async getSkillBankStats(): Promise<SkillBankStatsResponse> {
    return this.apiService.get<SkillBankStatsResponse>('/stats/skill-banks');
  }

  async getJobSourceStats(): Promise<JobSourceStatsResponse> {
    return this.apiService.get<JobSourceStatsResponse>('/stats/job-sources');
  }
}