import type { Component } from 'solid-js';

const ResumeBuilderView: Component = () => {
  return (
    <div class="container mx-auto px-4 py-20">
      <div class="tabs tabs-boxed mb-6">
        <a class="tab tab-active">Resume List</a>
        <a class="tab">Builder</a>
        <a class="tab">Preview</a>
      </div>
      
      {/* Resume List View */}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Sample Resume Cards */}
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">Software Engineer Resume</h2>
            <p class="text-base-content/70 text-sm mb-4">Last updated: 2 days ago</p>
            <div class="card-actions justify-end">
              <button class="btn btn-outline btn-sm">Edit</button>
              <button class="btn btn-primary btn-sm">Preview</button>
            </div>
          </div>
        </div>
        
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">Product Manager Resume</h2>
            <p class="text-base-content/70 text-sm mb-4">Last updated: 1 week ago</p>
            <div class="card-actions justify-end">
              <button class="btn btn-outline btn-sm">Edit</button>
              <button class="btn btn-primary btn-sm">Preview</button>
            </div>
          </div>
        </div>
        
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
    </div>
  );
};

export default ResumeBuilderView;