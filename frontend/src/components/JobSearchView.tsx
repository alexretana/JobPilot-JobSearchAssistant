import type { Component } from 'solid-js';
import { createSignal, onMount } from 'solid-js';
import { Job } from '../types/job';
import JobDetailsModal from './JobDetailsModal';
import { JobService } from '../services/JobService';

const jobService = new JobService();

// Transform backend job data to frontend job data
const transformJob = (backendJob: any): Job => {
  return {
    id: backendJob.job_id,
    title: backendJob.title,
    company: backendJob.company,
    location: backendJob.location,
    salary: jobService.formatSalary(backendJob.salary_min, backendJob.salary_max),
    type: backendJob.job_type,
    remote: backendJob.remote_type === 'Remote',
    hybrid: backendJob.remote_type === 'Hybrid',
    description: backendJob.description || '',
    skills: backendJob.skills || [],
    isSaved: false, // This would need to come from user data
    url: backendJob.url || '#'
  };
};

const JobSearchView: Component = () => {
  const [jobs, setJobs] = createSignal<Job[]>([]);
  const [loading, setLoading] = createSignal<boolean>(true);
  const [error, setError] = createSignal<string | null>(null);
  const [activeTab, setActiveTab] = createSignal<'jobs' | 'applications' | 'leads'>('jobs');
  const [selectedJob, setSelectedJob] = createSignal<Job | null>(null);

  // Fetch jobs from backend
  const fetchJobs = async () => {
    try {
      setLoading(true);
      setError(null);
      // Use searchJobs with no filters to get all jobs
      const response = await jobService.searchJobs({});
      const transformedJobs = response.results ? response.results.map(transformJob) : [];
      setJobs(transformedJobs);
    } catch (err: any) {
      setError(`Failed to load jobs: ${err.message || 'Please try again later.'}`);
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  onMount(() => {
    fetchJobs();
  });

  const handleSaveJob = (id: string) => {
    setJobs(jobs().map(job => 
      job.id === id ? { ...job, isSaved: !job.isSaved } : job
    ));
  };

  const handleVisitJob = (url: string) => {
    window.open(url, '_blank');
  };

  const handleViewDetails = (job: Job) => {
    setSelectedJob(job);
  };

  const handleCloseModal = () => {
    setSelectedJob(null);
  };

  return (
    <div class="container mx-auto px-4 py-20">
      <div class="tabs tabs-boxed mb-6">
        <a 
          class={`tab ${activeTab() === 'jobs' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('jobs')}
        >
          Jobs
        </a>
        <a 
          class={`tab ${activeTab() === 'applications' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('applications')}
        >
          Applications
        </a>
        <a 
          class={`tab ${activeTab() === 'leads' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('leads')}
        >
          Leads
        </a>
      </div>
      
      {activeTab() === 'jobs' && (
        <div>
          {loading() && (
            <div class="text-center py-10">
              <div class="loading loading-spinner loading-lg"></div>
              <p class="mt-4">Loading jobs...</p>
            </div>
          )}
          
          {error() && (
            <div class="alert alert-error mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error()}</span>
            </div>
          )}
          
          {!loading() && !error() && (
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {jobs().map((job) => (
                <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300">
                  <div class="card-body">
                    <h2 class="card-title">{job.title}</h2>
                    <div class="flex items-center text-sm text-base-content/70 mb-2">
                      <span>{job.company}</span>
                      <span class="mx-2">•</span>
                      <span>{job.location}</span>
                    </div>
                    <div class="flex items-center text-sm mb-3">
                      <span class="badge badge-primary mr-2">{job.salary}</span>
                      {job.remote && <span class="badge badge-secondary mr-2">Remote</span>}
                      {job.hybrid && <span class="badge badge-secondary">Hybrid</span>}
                    </div>
                    <p class="text-base-content/80 mb-4">
                      {job.description}
                    </p>
                    <div class="flex flex-wrap gap-2 mb-4">
                      {job.skills.slice(0, 3).map((skill) => (
                        <span class="badge badge-outline">{skill}</span>
                      ))}
                      {job.skills.length > 3 && (
                        <span class="badge badge-outline">+{job.skills.length - 3} more</span>
                      )}
                    </div>
                    <div class="card-actions justify-between">
                      <button 
                        class={`btn ${job.isSaved ? 'btn-active' : 'btn-outline'} btn-sm`}
                        onClick={() => handleSaveJob(job.id)}
                      >
                        {job.isSaved ? 'Saved' : 'Save'}
                      </button>
                      <div class="space-x-2">
                        <button 
                          class="btn btn-primary btn-sm"
                          onClick={() => handleVisitJob(job.url)}
                        >
                          Visit
                        </button>
                        <button 
                          class="btn btn-secondary btn-sm"
                          onClick={() => handleViewDetails(job)}
                        >
                          Details
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      {activeTab() === 'applications' && (
        <div class="text-center py-10">
          <h2 class="text-2xl font-bold mb-2">Job Applications</h2>
          <p class="text-base-content/70">Track your job applications here</p>
        </div>
      )}
      
      {activeTab() === 'leads' && (
        <div class="text-center py-10">
          <h2 class="text-2xl font-bold mb-2">Job Leads</h2>
          <p class="text-base-content/70">Manage your potential job opportunities</p>
        </div>
      )}
      
      <JobDetailsModal 
        job={selectedJob()}
        isOpen={!!selectedJob()}
        onClose={handleCloseModal}
        onSave={handleSaveJob}
        onVisit={handleVisitJob}
      />
    </div>
  );
};

export default JobSearchView;