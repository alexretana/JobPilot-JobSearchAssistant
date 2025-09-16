import type { Component } from 'solid-js';
import { createSignal, createEffect } from 'solid-js';
import type { Job } from '../types/job';
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

interface JobDetailsModalProps {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (id: string) => void;
  onVisit: (url: string) => void;
}

const JobDetailsModal: Component<JobDetailsModalProps> = (props) => {
  const [modalJob, setModalJob] = createSignal<Job | null>(null);
  const [loading, setLoading] = createSignal<boolean>(false);
  const [error, setError] = createSignal<string | null>(null);

  // Fetch detailed job information when job ID changes
  createEffect(async () => {
    if (props.job && props.isOpen) {
      // If we already have full job details, use them
      if (props.job.description && props.job.skills.length > 0) {
        setModalJob(props.job);
        return;
      }
      
      // Otherwise fetch detailed job info from backend
      try {
        setLoading(true);
        setError(null);
        const jobId = props.job.id;
        const response = await jobService.getJob(jobId);
        const transformedJob = transformJob(response);
        setModalJob(transformedJob);
      } catch (err) {
        setError('Failed to load job details. Please try again.');
        console.error('Error fetching job details:', err);
        setModalJob(props.job); // Fallback to the basic job info
      } finally {
        setLoading(false);
      }
    } else {
      setModalJob(null);
    }
  });

  return (
    <div class={`modal ${props.isOpen ? 'modal-open' : ''}`}>
      <div class="modal-box max-w-3xl">
        {loading() && (
          <div class="text-center py-10">
            <div class="loading loading-spinner loading-lg"></div>
            <p class="mt-4">Loading job details...</p>
          </div>
        )}
        
        {error() && (
          <div class="alert alert-warning mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span>{error()}</span>
          </div>
        )}
        
        {modalJob() && !loading() && (
          <>
            <div class="flex justify-between items-start mb-4">
              <div>
                <h2 class="text-2xl font-bold">{modalJob()!.title}</h2>
                <div class="flex items-center text-base-content/70 mt-1">
                  <span>{modalJob()!.company}</span>
                  <span class="mx-2">•</span>
                  <span>{modalJob()!.location}</span>
                </div>
              </div>
              <button class="btn btn-sm btn-circle" onClick={props.onClose}>
                ✕
              </button>
            </div>
            
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="badge badge-primary">{modalJob()!.salary}</span>
              {modalJob()!.remote && <span class="badge badge-secondary">Remote</span>}
              {modalJob()!.hybrid && <span class="badge badge-secondary">Hybrid</span>}
              <span class="badge badge-accent">{modalJob()!.type}</span>
            </div>
            
            <div class="mb-6">
              <h3 class="font-bold text-lg mb-2">Description</h3>
              <p class="text-base-content/80">{modalJob()!.description}</p>
            </div>
            
            <div class="mb-6">
              <h3 class="font-bold text-lg mb-2">Required Skills</h3>
              <div class="flex flex-wrap gap-2">
                {modalJob()!.skills.map((skill) => (
                  <span class="badge badge-outline badge-lg">{skill}</span>
                ))}
              </div>
            </div>
            
            <div class="modal-action">
              <button 
                class={`btn ${modalJob()!.isSaved ? 'btn-active' : 'btn-outline'}`}
                onClick={() => props.onSave(modalJob()!.id)}
              >
                {modalJob()!.isSaved ? 'Saved' : 'Save Job'}
              </button>
              <button 
                class="btn btn-primary"
                onClick={() => props.onVisit(modalJob()!.url)}
              >
                Visit Posting
              </button>
              <button class="btn" onClick={props.onClose}>Close</button>
            </div>
          </>
        )}
        
        {!modalJob() && !loading() && (
          <div class="text-center py-10">
            <h3 class="text-xl font-bold mb-2">No job selected</h3>
            <p class="text-base-content/70">Please select a job to view details</p>
            <div class="modal-action justify-center">
              <button class="btn" onClick={props.onClose}>Close</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobDetailsModal;