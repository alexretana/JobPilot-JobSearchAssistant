// SkillBank types
export interface SkillBank {
  id: string;
  user_id: string;
  skills: Skill[];
  summaries: ProfessionalSummary[];
  experiences: WorkExperience[];
  education: Education[];
  projects: Project[];
  certifications: Certification[];
  created_at: string;
  updated_at: string;
}

export interface Skill {
  id: string;
  name: string;
  level: SkillLevel;
  category: SkillCategory;
  years_of_experience: number;
  last_used: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface ProfessionalSummary {
  id: string;
  title: string;
  content: string;
  focus_type: ContentFocusType;
  created_at: string;
  updated_at: string;
}

export interface WorkExperience {
  id: string;
  company: string;
  position: string;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string;
  achievements: string[];
  skills_used: string[];
  created_at: string;
  updated_at: string;
}

export interface Education {
  id: string;
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date: string | null;
  gpa: number | null;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  start_date: string;
  end_date: string | null;
  is_ongoing: boolean;
  technologies: string[];
  url: string | null;
  achievements: string[];
  created_at: string;
  updated_at: string;
}

export interface Certification {
  id: string;
  name: string;
  issuing_organization: string;
  issue_date: string;
  expiration_date: string | null;
  credential_id: string | null;
  credential_url: string | null;
  description: string;
  created_at: string;
  updated_at: string;
}

export enum SkillLevel {
  BEGINNER = 'BEGINNER',
  INTERMEDIATE = 'INTERMEDIATE',
  ADVANCED = 'ADVANCED',
  EXPERT = 'EXPERT'
}

export enum SkillCategory {
  TECHNICAL = 'TECHNICAL',
  SOFT = 'SOFT',
  LANGUAGE = 'LANGUAGE',
  INDUSTRY = 'INDUSTRY'
}

export enum ContentFocusType {
  CAREER = 'CAREER',
  INDUSTRY = 'INDUSTRY',
  ROLE = 'ROLE'
}

// Alias for WorkExperience to match ExperienceType usage
export type ExperienceType = WorkExperience;