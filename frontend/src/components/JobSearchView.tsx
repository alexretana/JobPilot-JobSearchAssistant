import type { Component } from 'solid-js';

const JobSearchView: Component = () => {
  return (
    <div class="container mx-auto px-4 py-20">
      <div class="tabs tabs-boxed mb-6">
        <a class="tab tab-active">Jobs</a>
        <a class="tab">Applications</a>
        <a class="tab">Leads</a>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Sample Job Cards */}
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">Senior Software Engineer</h2>
            <div class="flex items-center text-sm text-base-content/70 mb-2">
              <span>Google</span>
              <span class="mx-2">•</span>
              <span>San Francisco, CA</span>
            </div>
            <div class="flex items-center text-sm mb-3">
              <span class="badge badge-primary mr-2">$120k - $150k</span>
              <span class="badge badge-secondary">Remote</span>
            </div>
            <p class="text-base-content/80 mb-4">
              We're looking for an experienced software engineer to join our team...
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="badge badge-outline">JavaScript</span>
              <span class="badge badge-outline">React</span>
              <span class="badge badge-outline">Node.js</span>
            </div>
            <div class="card-actions justify-between">
              <button class="btn btn-outline btn-sm">Save</button>
              <div class="space-x-2">
                <button class="btn btn-primary btn-sm">Apply</button>
                <button class="btn btn-secondary btn-sm">Details</button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">Product Manager</h2>
            <div class="flex items-center text-sm text-base-content/70 mb-2">
              <span>Microsoft</span>
              <span class="mx-2">•</span>
              <span>Seattle, WA</span>
            </div>
            <div class="flex items-center text-sm mb-3">
              <span class="badge badge-primary mr-2">$130k - $160k</span>
            </div>
            <p class="text-base-content/80 mb-4">
              Join our product team to help shape the future of our cloud platform...
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="badge badge-outline">Product Strategy</span>
              <span class="badge badge-outline">Agile</span>
              <span class="badge badge-outline">Analytics</span>
            </div>
            <div class="card-actions justify-between">
              <button class="btn btn-outline btn-sm">Save</button>
              <div class="space-x-2">
                <button class="btn btn-primary btn-sm">Apply</button>
                <button class="btn btn-secondary btn-sm">Details</button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">UX Designer</h2>
            <div class="flex items-center text-sm text-base-content/70 mb-2">
              <span>Apple</span>
              <span class="mx-2">•</span>
              <span>Cupertino, CA</span>
            </div>
            <div class="flex items-center text-sm mb-3">
              <span class="badge badge-primary mr-2">$110k - $140k</span>
              <span class="badge badge-secondary">Hybrid</span>
            </div>
            <p class="text-base-content/80 mb-4">
              Create beautiful and intuitive user experiences for our next generation products...
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="badge badge-outline">Figma</span>
              <span class="badge badge-outline">Prototyping</span>
              <span class="badge badge-outline">User Research</span>
            </div>
            <div class="card-actions justify-between">
              <button class="btn btn-outline btn-sm btn-active">Saved</button>
              <div class="space-x-2">
                <button class="btn btn-primary btn-sm">Apply</button>
                <button class="btn btn-secondary btn-sm">Details</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobSearchView;