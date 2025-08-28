// Mock data for testing UserProfile components

export const mockUserProfile = {
  id: 'test-user-123',
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@example.com',
  phone: '+1 (555) 123-4567',
  city: 'San Francisco',
  state: 'CA',
  linkedin_url: 'https://linkedin.com/in/johndoe',
  portfolio_url: 'https://johndoe.com',
  current_title: 'Senior Software Engineer',
  experience_years: 5,
  skills: ['JavaScript', 'TypeScript', 'React', 'Node.js'],
  education: 'B.S. Computer Science',
  bio: 'Passionate software engineer with 5 years of experience building web applications.',
  preferred_locations: ['San Francisco, CA', 'New York, NY', 'Remote'],
  preferred_job_types: ['Full-time'],
  preferred_remote_types: ['Remote', 'Hybrid'],
  desired_salary_min: 120000,
  desired_salary_max: 150000,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z'
};

export const mockJob = {
  job_id: 'job-123',
  title: 'Senior Software Engineer',
  company: 'Tech Corp',
  location: 'San Francisco, CA',
  job_type: 'Full-time',
  remote_type: 'Remote',
  experience_level: 'Senior',
  salary_min: 120000,
  salary_max: 150000,
  posted_date: '2023-01-01T00:00:00Z'
};

export const mockSkillBank = {
  id: 'skillbank-123',
  user_id: 'test-user-123',
  skills: [
    {
      id: 'skill-1',
      name: 'JavaScript',
      level: 'Expert',
      category: 'Programming Languages',
      years_experience: 5
    },
    {
      id: 'skill-2',
      name: 'React',
      level: 'Expert',
      category: 'Frameworks',
      years_experience: 4
    }
  ],
  work_experiences: [
    {
      id: 'exp-1',
      company: 'Tech Corp',
      position: 'Senior Software Engineer',
      location: 'San Francisco, CA',
      start_date: '2020-01-01',
      end_date: '2023-01-01',
      is_current: false
    }
  ],
  education_entries: [
    {
      id: 'edu-1',
      institution: 'University of California',
      degree: 'B.S. Computer Science',
      field_of_study: 'Computer Science',
      location: 'Berkeley, CA',
      start_date: '2016-08-01',
      graduation_date: '2020-05-01'
    }
  ],
  projects: [
    {
      id: 'proj-1',
      name: 'Job Search Platform',
      description: 'A platform to help job seekers find their dream job',
      technologies: ['React', 'Node.js', 'MongoDB'],
      url: 'https://github.com/example/job-search-platform'
    }
  ],
  certifications: [
    {
      id: 'cert-1',
      name: 'AWS Certified Solutions Architect',
      issuer: 'Amazon Web Services',
      date_earned: '2022-01-01'
    }
  ],
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z'
};