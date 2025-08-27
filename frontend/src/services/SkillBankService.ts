// frontend/src/services/SkillBankService.ts
import { ApiService } from './ApiService';

// Define types for skill banks
export interface EnhancedSkill {
  id?: string;
  name: string;
  level?: string;
  category?: string;
  subcategory?: string;
  years_experience?: number;
  proficiency_score?: number;
  description?: string;
  keywords?: string[];
  is_featured?: boolean;
  display_order?: number;
  created_at?: string;
  updated_at?: string;
}

export interface ExperienceEntry {
  id?: string;
  company: string;
  position: string;
  location?: string;
  start_date: string;
  end_date?: string;
  is_current?: boolean;
  default_description?: string;
  default_achievements?: string[];
  skills_used?: string[];
  technologies?: string[];
  created_at?: string;
  updated_at?: string;
}

export interface EducationEntry {
  id?: string;
  institution: string;
  degree: string;
  field_of_study?: string;
  location?: string;
  start_date?: string;
  graduation_date?: string;
  gpa?: string;
  honors?: string[];
  relevant_coursework?: string[];
  created_at?: string;
  updated_at?: string;
}

export interface ProjectEntry {
  id?: string;
  name: string;
  description?: string;
  technologies?: string[];
  url?: string;
  start_date?: string;
  end_date?: string;
  achievements?: string[];
  created_at?: string;
  updated_at?: string;
}

export interface Certification {
  id?: string;
  name: string;
  issuer?: string;
  date_earned?: string;
  expiry_date?: string;
  credential_id?: string;
  verification_url?: string;
  status?: string;
  created_at?: string;
  updated_at?: string;
}

export interface SummaryVariation {
  id?: string;
  title: string;
  content: string;
  is_primary?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface ExperienceContentVariation {
  id?: string;
  experience_id: string;
  title: string;
  content: string;
  is_primary?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface SkillBank {
  id: string;
  user_id: string;
  skills: EnhancedSkill[];
  skill_categories?: Record<string, number>;
  default_summary?: string;
  summary_variations?: SummaryVariation[];
  work_experiences?: ExperienceEntry[];
  education_entries?: EducationEntry[];
  projects?: ProjectEntry[];
  certifications?: Certification[];
  experience_content_variations?: ExperienceContentVariation[];
  created_at: string;
  updated_at: string;
}

export interface SkillBankCreate {
  user_id: string;
  initial_skills?: EnhancedSkill[];
  default_summary?: string;
}

export interface SkillBankUpdate {
  default_summary?: string;
  summary_variations?: SummaryVariation[];
}

export interface SkillCreate {
  name: string;
  level?: string;
  category?: string;
  subcategory?: string;
  years_experience?: number;
  proficiency_score?: number;
  description?: string;
  keywords?: string[];
  is_featured?: boolean;
  display_order?: number;
}

export interface SkillUpdate {
  level?: string;
  category?: string;
  subcategory?: string;
  years_experience?: number;
  proficiency_score?: number;
  description?: string;
  keywords?: string[];
  is_featured?: boolean;
  display_order?: number;
}

export interface ExperienceCreate {
  company: string;
  position: string;
  location?: string;
  start_date: string;
  end_date?: string;
  is_current?: boolean;
  default_description?: string;
  default_achievements?: string[];
  skills_used?: string[];
  technologies?: string[];
}

export interface ExperienceUpdate {
  company?: string;
  position?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  is_current?: boolean;
  default_description?: string;
  default_achievements?: string[];
  skills_used?: string[];
  technologies?: string[];
}

export interface SkillBankResponse extends SkillBank {}

export class SkillBankService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async createSkillBank(skillBankData: SkillBankCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>('/skill-banks', skillBankData);
  }

  async getSkillBank(userId: string): Promise<SkillBankResponse> {
    return this.apiService.get<SkillBankResponse>(`/skill-banks/${userId}`);
  }

  async updateSkillBank(userId: string, updateData: SkillBankUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}`, updateData);
  }

  async deleteSkillBank(userId: string): Promise<{ message: string }> {
    return this.apiService.delete<{ message: string }>(`/skill-banks/${userId}`);
  }

  async addSkill(userId: string, skillData: SkillCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>(`/skill-banks/${userId}/skills`, skillData);
  }

  async updateSkill(userId: string, skillId: string, updateData: SkillUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}/skills/${skillId}`, updateData);
  }

  async deleteSkill(userId: string, skillId: string): Promise<SkillBankResponse> {
    return this.apiService.delete<SkillBankResponse>(`/skill-banks/${userId}/skills/${skillId}`);
  }

  async addExperience(userId: string, experienceData: ExperienceCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>(`/skill-banks/${userId}/experiences`, experienceData);
  }

  async updateExperience(userId: string, experienceId: string, updateData: ExperienceUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}/experiences/${experienceId}`, updateData);
  }

  async deleteExperience(userId: string, experienceId: string): Promise<SkillBankResponse> {
    return this.apiService.delete<SkillBankResponse>(`/skill-banks/${userId}/experiences/${experienceId}`);
  }
}