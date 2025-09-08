// frontend/src/services/JobService.ts
import { apiService } from './ApiService';

// Define types for jobs
export interface Job {
  job_id: string;
  title: string;
  company: string;
  location: string;
  job_type: string;
  remote_type: string;
  experience_level: string;
  salary_min?: number;
  salary_max?: number;
  posted_date: string;
  [key: string]: any; // Allow additional properties
}

export interface JobSearchFilters {
  query?: string;
  job_type?: string;
  remote_type?: string;
  experience_level?: string;
  salary_min?: number;
  salary_max?: number;
  location?: string;
  company?: string;
  posted_after?: string;
  posted_before?: string;
}

export interface JobSearchResponse {
  message: string;
  user_id: string;
  filters_applied: Record<string, any>;
  results: Job[];
  total_results: number;
  page: number;
  page_size: number;
}

export interface JobStatisticsResponse {
  message: string;
  user_id: string;
  total_jobs: number;
  jobs_by_type: Record<string, number>;
  jobs_by_remote_type: Record<string, number>;
  jobs_by_experience_level: Record<string, number>;
  average_salary_by_type: Record<string, { min: number; max: number }>;
  top_locations: Array<{ location: string; count: number }>;
  top_companies: Array<{ company: string; count: number }>;
  recent_trend: { last_7_days: number; last_30_days: number; last_90_days: number };
}

export class JobService {
  private apiService = apiService;

  async searchJobs(filters: JobSearchFilters): Promise<JobSearchResponse> {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined) {
        params.append(key, value.toString());
      }
    });
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiService.get<JobSearchResponse>(`/jobs/search${queryString}`);
  }

  async getJobStatistics(): Promise<JobStatisticsResponse> {
    return this.apiService.get<JobStatisticsResponse>('/jobs/statistics');
  }

  async listJobs(): Promise<any> {
    return this.apiService.get<any>('/jobs');
  }

  async getJob(jobId: string): Promise<any> {
    return this.apiService.get<any>(`/jobs/${jobId}`);
  }

  async createJob(): Promise<any> {
    return this.apiService.post<any>('/jobs');
  }

  async updateJob(jobId: string): Promise<any> {
    return this.apiService.put<any>(`/jobs/${jobId}`);
  }

  async deleteJob(jobId: string): Promise<any> {
    return this.apiService.delete<any>(`/jobs/${jobId}`);
  }

  /**
   * Format salary range for display
   */
  formatSalary(salary_min?: number, salary_max?: number): string {
    if (!salary_min && !salary_max) {
      return 'Salary not specified';
    }

    if (salary_min && salary_max) {
      return `$${salary_min.toLocaleString()} - $${salary_max.toLocaleString()}`;
    }

    if (salary_min) {
      return `$${salary_min.toLocaleString()}+`;
    }

    if (salary_max) {
      return `Up to $${salary_max.toLocaleString()}`;
    }

    return 'Salary not specified';
  }

  /**
   * Format posted date for display
   */
  formatPostedDate(posted_date: string | null): string {
    if (!posted_date) {
      return 'Date not specified';
    }

    const date = new Date(posted_date);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return '1 day ago';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else if (diffDays < 30) {
      const weeks = Math.floor(diffDays / 7);
      return weeks === 1 ? '1 week ago' : `${weeks} weeks ago`;
    } else {
      return date.toLocaleDateString();
    }
  }

  /**
   * Get job type display label
   */
  getJobTypeLabel(jobType: string | null): string {
    if (!jobType) return 'Not specified';

    const labels: Record<string, string> = {
      'Full-time': 'Full-time',
      'Part-time': 'Part-time',
      Contract: 'Contract',
      Temporary: 'Temporary',
      Internship: 'Internship',
      Volunteer: 'Volunteer',
    };

    return labels[jobType] || jobType;
  }

  /**
   * Get remote type display label
   */
  getRemoteTypeLabel(remoteType: string | null): string {
    if (!remoteType) return 'Not specified';

    const labels: Record<string, string> = {
      Remote: 'Remote',
      'On-site': 'On-site',
      Hybrid: 'Hybrid',
    };

    return labels[remoteType] || remoteType;
  }

  /**
   * Get remote type icon
   */
  getRemoteTypeIcon(remoteType: string | null): string {
    const icons: Record<string, string> = {
      Remote: '🏠',
      'On-site': '🏢',
      Hybrid: '🔄',
    };

    return icons[remoteType || ''] || '📍';
  }
}