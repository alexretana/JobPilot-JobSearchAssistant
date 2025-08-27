// frontend/src/services/UserProfileService.ts
import { ApiService } from './ApiService';

// Define types for user profiles
export interface UserProfile {
  id: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  current_title?: string;
  experience_years?: number;
  skills: string[];
  education?: string;
  bio?: string;
  preferred_locations: string[];
  preferred_job_types: JobType[];
  preferred_remote_types: RemoteType[];
  desired_salary_min?: number;
  desired_salary_max?: number;
  created_at: string;
  updated_at: string;
}

export type JobType =
  | 'Full-time'
  | 'Part-time'
  | 'Contract'
  | 'Freelance'
  | 'Internship'
  | 'Temporary';

export type RemoteType = 'On-site' | 'Remote' | 'Hybrid';

export interface UserProfileCreate {
  first_name?: string;
  last_name: string; // Required
  email: string; // Required (EmailStr)
  phone?: string;
  city?: string;
  state?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  current_title?: string;
  experience_years?: number;
  skills: string[]; // Required (non-empty)
  education?: string;
  bio?: string;
  preferred_locations?: string[];
  preferred_job_types: JobType[]; // Required (non-empty)
  preferred_remote_types: RemoteType[]; // Required (non-empty)
  desired_salary_min?: number;
  desired_salary_max?: number;
}

export interface UserProfileUpdate {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  current_title?: string;
  experience_years?: number;
  skills?: string[];
  education?: string;
  bio?: string;
  preferred_locations?: string[];
  preferred_job_types?: JobType[];
  preferred_remote_types?: RemoteType[];
  desired_salary_min?: number;
  desired_salary_max?: number;
}

export class UserProfileService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async createProfile(profileData: UserProfileCreate): Promise<UserProfile> {
    return this.apiService.post<UserProfile>('/users', profileData);
  }

  async getProfile(userId: string): Promise<UserProfile> {
    return this.apiService.get<UserProfile>(`/users/${userId}`);
  }

  async getDefaultProfile(): Promise<UserProfile> {
    return this.apiService.get<UserProfile>('/users/default');
  }

  async updateProfile(userId: string, updates: UserProfileUpdate): Promise<UserProfile> {
    return this.apiService.put<UserProfile>(`/users/${userId}`, updates);
  }

  async deleteProfile(userId: string): Promise<{ message: string }> {
    return this.apiService.delete<{ message: string }>(`/users/${userId}`);
  }

  async listProfiles(limit: number = 20, offset: number = 0): Promise<UserProfile[]> {
    return this.apiService.get<UserProfile[]>(`/users?limit=${limit}&offset=${offset}`);
  }

  async searchProfileByEmail(email: string): Promise<UserProfile> {
    return this.apiService.get<UserProfile>(`/users/search/by-email?email=${encodeURIComponent(email)}`);
  }
}