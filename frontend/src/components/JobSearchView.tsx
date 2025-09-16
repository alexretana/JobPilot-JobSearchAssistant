import type { Component } from 'solid-js';
import { createSignal } from 'solid-js';
import { Job, sampleJobs } from '../types/job';
import JobDetailsModal from './JobDetailsModal';

const JobSearchView: Component = () => {
  const [jobs, setJobs] = createSignal<Job[]>(sampleJobs);
  const [activeTab, setActiveTab] = createSignal<'jobs' | 'applications' | 'leads'>('jobs');
  const [selectedJob, setSelectedJob] = createSignal<Job | null>(null);

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