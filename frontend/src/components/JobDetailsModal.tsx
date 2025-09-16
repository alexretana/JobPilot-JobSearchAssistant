import type { Component } from 'solid-js';
import type { Job } from '../types/job';

interface JobDetailsModalProps {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (id: string) => void;
  onVisit: (url: string) => void;
}

const JobDetailsModal: Component<JobDetailsModalProps> = (props) => {
  return (
    <div class={`modal ${props.isOpen && props.job ? 'modal-open' : ''}`}>
      <div class="modal-box max-w-3xl">
        {props.job && (
          <>
            <div class="flex justify-between items-start mb-4">
              <div>
                <h2 class="text-2xl font-bold">{props.job.title}</h2>
                <div class="flex items-center text-base-content/70 mt-1">
                  <span>{props.job.company}</span>
                  <span class="mx-2">•</span>
                  <span>{props.job.location}</span>
                </div>
              </div>
              <button class="btn btn-sm btn-circle" onClick={props.onClose}>
                ✕
              </button>
            </div>
            
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="badge badge-primary">{props.job.salary}</span>
              {props.job.remote && <span class="badge badge-secondary">Remote</span>}
              {props.job.hybrid && <span class="badge badge-secondary">Hybrid</span>}
              <span class="badge badge-accent">{props.job.type}</span>
            </div>
            
            <div class="mb-6">
              <h3 class="font-bold text-lg mb-2">Description</h3>
              <p class="text-base-content/80">{props.job.description}</p>
            </div>
            
            <div class="mb-6">
              <h3 class="font-bold text-lg mb-2">Required Skills</h3>
              <div class="flex flex-wrap gap-2">
                {props.job.skills.map((skill) => (
                  <span class="badge badge-outline badge-lg">{skill}</span>
                ))}
              </div>
            </div>
            
            <div class="modal-action">
              <button 
                class={`btn ${props.job.isSaved ? 'btn-active' : 'btn-outline'}`}
                onClick={() => props.onSave(props.job!.id)}
              >
                {props.job.isSaved ? 'Saved' : 'Save Job'}
              </button>
              <button 
                class="btn btn-primary"
                onClick={() => props.onVisit(props.job!.url)}
              >
                Visit Posting
              </button>
              <button class="btn" onClick={props.onClose}>Close</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default JobDetailsModal;