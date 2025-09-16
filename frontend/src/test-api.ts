// Simple test file to verify API connectivity
import { JobService } from './services/JobService';
import { initializeDevAuth } from './services/AuthUtils';

// Initialize auth
initializeDevAuth();

// Create job service instance
const jobService = new JobService();

// Test the API
const testApi = async () => {
  try {
    console.log('Testing API connectivity...');
    const jobs = await jobService.listJobs();
    console.log('Jobs API response:', jobs);
  } catch (error) {
    console.error('API test failed:', error);
  }
};

testApi();