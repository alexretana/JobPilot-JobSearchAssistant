import type { Component } from 'solid-js';
import { createSignal, onMount } from 'solid-js';
import { ResumeService } from '../services/ResumeService';

const resumeService = new ResumeService();

const ResumeBuilderView: Component = () => {
  const [resumes, setResumes] = createSignal<any[]>([]);
  const [loading, setLoading] = createSignal<boolean>(true);
  const [error, setError] = createSignal<string | null>(null);

  // Fetch resumes from the service
  const fetchResumes = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await resumeService.listResumes();
      setResumes(response.resumes);
    } catch (err: any) {
      // If we get an error, try to use mock data
      console.error('Error fetching resumes:', err);
      setError(`Failed to load resumes: ${err.message || 'Please try again later.'}`);
      
      // Use mock data as fallback
      setResumes([
        {
          id: '1',
          title: 'Software Engineer Resume',
          updated_at: new Date().toISOString()
        },
        {
          id: '2',
          title: 'Product Manager Resume',
          updated_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString() // 1 week ago
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  onMount(() => {
    fetchResumes();
  });

  return (
    <div class="container mx-auto px-4 py-20">
      <div class="tabs tabs-boxed mb-6">
        <a class="tab tab-active">Resume List</a>
        <a class="tab">Builder</a>
        <a class="tab">Preview</a>
      </div>
      
      {/* Loading state */}
      {loading() && (
        <div class="text-center py-10">
          <div class="loading loading-spinner loading-lg"></div>
          <p class="mt-4">Loading resumes...</p>
        </div>
      )}
      
      {/* Error state */}
      {error() && (
        <div class="alert alert-warning mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span>{error()}</span>
        </div>
      )}
      
      {/* Resume List View */}
      {!loading() && (
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Resume Cards from API or mock data */}
          {resumes().map((resume) => (
            <div class="card bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title">{resume.title}</h2>
                <p class="text-base-content/70 text-sm mb-4">
                  Last updated: {new Date(resume.updated_at).toLocaleDateString()}
                </p>
                <div class="card-actions justify-end">
                  <button class="btn btn-outline btn-sm">Edit</button>
                  <button class="btn btn-primary btn-sm">Preview</button>
                </div>
              </div>
            </div>
          ))}
          
          {/* Create New Resume Card */}
          <div class="card bg-base-100 shadow-xl border-2 border-dashed border-base-content/30">
            <div class="card-body flex items-center justify-center">
              <button class="btn btn-primary btn-circle btn-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
              <h3 class="text-lg font-semibold mt-4">Create New Resume</h3>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeBuilderView;