// frontend/src/services/ResumeService.ts
import { apiService } from './ApiService';

// Define types for resumes
export interface ResumeContactInfo {
  full_name: string;
  email: string;
  phone?: string;
  location?: string;
  linkedin_url?: string;
  github_url?: string;
  website_url?: string;
}

export interface ResumeWorkExperience {
  company: string;
  position: string;
  location?: string;
  start_date: string;
  end_date?: string;
  is_current?: boolean;
  description?: string;
  achievements?: string[];
}

export interface ResumeEducation {
  institution: string;
  degree: string;
  field_of_study?: string;
  location?: string;
  start_date?: string;
  graduation_date?: string;
  gpa?: string;
  honors?: string[];
  relevant_coursework?: string[];
}

export interface ResumeSkill {
  name: string;
  category?: string;
  proficiency_level?: string;
}

export interface ResumeProject {
  name: string;
  description?: string;
  technologies?: string[];
  url?: string;
  start_date?: string;
  end_date?: string;
  achievements?: string[];
}

export interface ResumeCertification {
  name: string;
  issuer?: string;
  date_earned?: string;
  expiry_date?: string;
  credential_id?: string;
  verification_url?: string;
  status?: string;
}

export interface Resume {
  id: string;
  user_id: string;
  title: string;
  status: string;
  resume_type: string;
  contact_info: ResumeContactInfo;
  summary?: string;
  work_experience?: ResumeWorkExperience[];
  education?: ResumeEducation[];
  skills?: ResumeSkill[];
  projects?: ResumeProject[];
  certifications?: ResumeCertification[];
  template_id?: string;
  parent_resume_id?: string;
  version: number;
  created_at: string;
  updated_at: string;
  last_generated_at?: string;
}

export interface ResumeCreate {
  user_id: string;
  title: string;
  resume_type: string;
  contact_info: ResumeContactInfo;
  summary?: string;
  work_experience?: ResumeWorkExperience[];
  education?: ResumeEducation[];
  skills?: ResumeSkill[];
  projects?: ResumeProject[];
  certifications?: ResumeCertification[];
  template_id?: string;
  parent_resume_id?: string;
}

export interface ResumeUpdate {
  title?: string;
  status?: string;
  resume_type?: string;
  contact_info?: ResumeContactInfo;
  summary?: string;
  work_experience?: ResumeWorkExperience[];
  education?: ResumeEducation[];
  skills?: ResumeSkill[];
  projects?: ResumeProject[];
  certifications?: ResumeCertification[];
  template_id?: string;
  parent_resume_id?: string;
}

export interface ResumeListResponse {
  resumes: Resume[];
  total: number;
  page: number;
  page_size: number;
}

export interface ResumeResponse extends Resume {}

export class ResumeService {
  private apiService = apiService;

  async listResumes(
    status?: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<ResumeListResponse> {
    const params = new URLSearchParams();
    
    if (status) {
      params.append('status', status);
    }
    
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    
    return this.apiService.get<ResumeListResponse>(`/resumes?${params.toString()}`);
  }

  async getResume(resumeId: string): Promise<ResumeResponse> {
    return this.apiService.get<ResumeResponse>(`/resumes/${resumeId}`);
  }

  async createResume(resumeData: ResumeCreate): Promise<ResumeResponse> {
    return this.apiService.post<ResumeResponse>('/resumes', resumeData);
  }

  async updateResume(resumeId: string, updateData: ResumeUpdate): Promise<ResumeResponse> {
    return this.apiService.put<ResumeResponse>(`/resumes/${resumeId}`, updateData);
  }

  async deleteResume(resumeId: string): Promise<{ message: string }> {
    return this.apiService.delete<{ message: string }>(`/resumes/${resumeId}`);
  }
}