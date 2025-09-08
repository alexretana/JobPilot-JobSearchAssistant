// frontend/src/services/SkillBankService.ts
import { apiService } from './ApiService';

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
  experience_type?: string;
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
  end_date?: string;
  default_description?: string;
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
  github_url?: string;
  default_description?: string;
  default_achievements?: string[];
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
  issue_date?: string;
  url?: string;
  description?: string;
}

export interface SummaryVariation {
  id?: string;
  title: string;
  content: string;
  is_primary?: boolean;
  created_at?: string;
  updated_at?: string;
  tone?: string;
  length?: string;
  focus?: string;
  target_industries?: string[];
  target_roles?: string[];
  keywords_emphasized?: string[];
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
  experience_type?: string;
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
  experience_type?: string;
}

export interface EducationCreate {
  institution: string;
  degree: string;
  field_of_study?: string;
  location?: string;
  start_date?: string;
  graduation_date?: string;
  gpa?: string;
  honors?: string[];
  relevant_coursework?: string[];
  end_date?: string;
  default_description?: string;
}

export interface EducationUpdate {
  institution?: string;
  degree?: string;
  field_of_study?: string;
  location?: string;
  start_date?: string;
  graduation_date?: string;
  gpa?: string;
  honors?: string[];
  relevant_coursework?: string[];
  end_date?: string;
  default_description?: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  technologies?: string[];
  url?: string;
  start_date?: string;
  end_date?: string;
  achievements?: string[];
  github_url?: string;
  default_description?: string;
  default_achievements?: string[];
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  technologies?: string[];
  url?: string;
  start_date?: string;
  end_date?: string;
  achievements?: string[];
  github_url?: string;
  default_description?: string;
  default_achievements?: string[];
}

export interface CertificationCreate {
  name: string;
  issuer?: string;
  date_earned?: string;
  expiry_date?: string;
  credential_id?: string;
  verification_url?: string;
  status?: string;
  issue_date?: string;
  url?: string;
  description?: string;
}

export interface CertificationUpdate {
  name?: string;
  issuer?: string;
  date_earned?: string;
  expiry_date?: string;
  credential_id?: string;
  verification_url?: string;
  status?: string;
  issue_date?: string;
  url?: string;
  description?: string;
}

export interface SummaryVariationCreate {
  title: string;
  content: string;
  is_primary?: boolean;
  tone?: string;
  length?: string;
  focus?: string;
  target_industries?: string[];
  target_roles?: string[];
  keywords_emphasized?: string[];
}

export interface SummaryVariationUpdate {
  title?: string;
  content?: string;
  is_primary?: boolean;
  tone?: string;
  length?: string;
  focus?: string;
  target_industries?: string[];
  target_roles?: string[];
  keywords_emphasized?: string[];
}

export interface ExperienceCreate {
  company: string;
  position: string;
  location?: string;
  start_date: string;
  end_date?: string;
  is_current?: boolean;
  experience_type?: string;
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
  experience_type?: string;
  default_description?: string;
  default_achievements?: string[];
  skills_used?: string[];
  technologies?: string[];
}

export interface EducationCreate {
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

export interface EducationUpdate {
  institution?: string;
  degree?: string;
  field_of_study?: string;
  location?: string;
  start_date?: string;
  graduation_date?: string;
  gpa?: string;
  honors?: string[];
  relevant_coursework?: string[];
}

export interface ProjectCreate {
  name: string;
  description?: string;
  technologies?: string[];
  url?: string;
  github_url?: string;
  start_date?: string;
  end_date?: string;
  achievements?: string[];
  default_description?: string;
  default_achievements?: string[];
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  technologies?: string[];
  url?: string;
  github_url?: string;
  start_date?: string;
  end_date?: string;
  achievements?: string[];
  default_description?: string;
  default_achievements?: string[];
}

export interface CertificationCreate {
  name: string;
  issuer?: string;
  date_earned?: string;
  expiry_date?: string;
  credential_id?: string;
  verification_url?: string;
  status?: string;
  issue_date?: string;
  url?: string;
  description?: string;
}

export interface CertificationUpdate {
  name?: string;
  issuer?: string;
  date_earned?: string;
  expiry_date?: string;
  credential_id?: string;
  verification_url?: string;
  status?: string;
  issue_date?: string;
  url?: string;
  description?: string;
}

export interface SummaryVariationCreate {
  title: string;
  content: string;
  is_primary?: boolean;
  tone?: string;
  length?: string;
  focus?: string;
  target_industries?: string[];
  target_roles?: string[];
  keywords_emphasized?: string[];
}

export interface SummaryVariationUpdate {
  title?: string;
  content?: string;
  is_primary?: boolean;
  tone?: string;
  length?: string;
  focus?: string;
  target_industries?: string[];
  target_roles?: string[];
  keywords_emphasized?: string[];
}

export interface SkillBankResponse extends SkillBank {}

export class SkillBankService {
  private apiService = apiService;

  async createSkillBank(skillBankData: any): Promise<SkillBankResponse> {
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

  async addEducation(userId: string, educationData: EducationCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>(`/skill-banks/${userId}/education`, educationData);
  }

  async updateEducation(userId: string, educationId: string, updateData: EducationUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}/education/${educationId}`, updateData);
  }

  async deleteEducation(userId: string, educationId: string): Promise<SkillBankResponse> {
    return this.apiService.delete<SkillBankResponse>(`/skill-banks/${userId}/education/${educationId}`);
  }

  async addProject(userId: string, projectData: ProjectCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>(`/skill-banks/${userId}/projects`, projectData);
  }

  async updateProject(userId: string, projectId: string, updateData: ProjectUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}/projects/${projectId}`, updateData);
  }

  async deleteProject(userId: string, projectId: string): Promise<SkillBankResponse> {
    return this.apiService.delete<SkillBankResponse>(`/skill-banks/${userId}/projects/${projectId}`);
  }

  async addCertification(userId: string, certificationData: CertificationCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>(`/skill-banks/${userId}/certifications`, certificationData);
  }

  async updateCertification(userId: string, certificationId: string, updateData: CertificationUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}/certifications/${certificationId}`, updateData);
  }

  async deleteCertification(userId: string, certificationId: string): Promise<SkillBankResponse> {
    return this.apiService.delete<SkillBankResponse>(`/skill-banks/${userId}/certifications/${certificationId}`);
  }

  async addSummaryVariation(userId: string, summaryData: SummaryVariationCreate): Promise<SkillBankResponse> {
    return this.apiService.post<SkillBankResponse>(`/skill-banks/${userId}/summary-variations`, summaryData);
  }

  async updateSummaryVariation(userId: string, summaryId: string, updateData: SummaryVariationUpdate): Promise<SkillBankResponse> {
    return this.apiService.put<SkillBankResponse>(`/skill-banks/${userId}/summary-variations/${summaryId}`, updateData);
  }

  async deleteSummaryVariation(userId: string, summaryId: string): Promise<SkillBankResponse> {
    return this.apiService.delete<SkillBankResponse>(`/skill-banks/${userId}/summary-variations/${summaryId}`);
  }
}