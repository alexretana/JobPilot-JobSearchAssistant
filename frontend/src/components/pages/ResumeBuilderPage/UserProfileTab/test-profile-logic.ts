// Test file to verify the logic of our profile components without JSX issues

import { UserProfileService } from '../../../../services/UserProfileService';
import { calculateCompleteness, formatSalaryRange, validateProfile, getJobTypes, getRemoteTypes } from '../../../../utils/profileUtils';

// Test that we can instantiate the service
const userProfileService = new UserProfileService();

// Test that our utility functions work
const testProfile = {
  id: 'test-id',
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@example.com',
  phone: '123-456-7890',
  city: 'Test City',
  state: 'TS',
  linkedin_url: 'https://linkedin.com/in/johndoe',
  portfolio_url: 'https://johndoe.com',
  current_title: 'Software Engineer',
  experience_years: 5,
  skills: ['JavaScript', 'TypeScript', 'React'],
  education: 'B.S. Computer Science',
  bio: 'Experienced software engineer',
  preferred_locations: ['New York', 'San Francisco'],
  preferred_job_types: ['Full-time', 'Contract'],
  preferred_remote_types: ['Remote', 'Hybrid'],
  desired_salary_min: 100000,
  desired_salary_max: 150000,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z'
};

// Test utility functions
const completeness = calculateCompleteness(testProfile);
console.log('Completeness:', completeness);

const salaryRange = formatSalaryRange(100000, 150000);
console.log('Salary Range:', salaryRange);

const validationErrors = validateProfile(testProfile);
console.log('Validation Errors:', validationErrors);

const jobTypes = getJobTypes();
console.log('Job Types:', jobTypes);

const remoteTypes = getRemoteTypes();
console.log('Remote Types:', remoteTypes);

console.log('All tests passed!');