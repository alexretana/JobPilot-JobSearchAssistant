import type { Component } from 'solid-js';
import { createSignal } from 'solid-js';
import { A } from '@solidjs/router';

const Header: Component = () => {
  const [isStatusPanelOpen, setIsStatusPanelOpen] = createSignal(false);

  const toggleStatusPanel = () => {
    setIsStatusPanelOpen(prev => !prev);
  };

  return (
    <header class="fixed top-0 left-0 right-0 z-50 bg-base-100 shadow-md">
      <div class="container mx-auto px-4 py-3">
        <div class="flex items-center justify-between">
          {/* Left side - Logo and Brand */}
          <div class="flex items-center space-x-2">
            <div class="bg-primary w-8 h-8 rounded-lg"></div>
            <span class="text-xl font-bold">JobPilot</span>
          </div>

          {/* Center - Navigation Tabs */}
          <nav class="hidden md:flex space-x-1">
            <A 
              href="/" 
              class="btn btn-ghost btn-sm rounded-btn"
              activeClass="btn-active"
            >
              AI Chat
            </A>
            <A 
              href="/job-search" 
              class="btn btn-ghost btn-sm rounded-btn"
              activeClass="btn-active"
            >
              Job Search
            </A>
            <A 
              href="/resume-builder" 
              class="btn btn-ghost btn-sm rounded-btn"
              activeClass="btn-active"
            >
              Resume Builder
            </A>
          </nav>

          {/* Right side - Status Panel Toggle */}
          <div class="flex items-center">
            {/* Status Panel Toggle */}
            <button 
              class="btn btn-ghost btn-sm"
              onClick={toggleStatusPanel}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* System Status Panel */}
      <div class={`fixed top-16 right-0 h-full w-80 bg-base-100 shadow-xl transform transition-transform duration-300 ease-in-out z-40 ${isStatusPanelOpen() ? 'translate-x-0' : 'translate-x-full'}`}>
        <div class="p-4 border-b border-base-200">
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold">System Status</h2>
            <button 
              class="btn btn-ghost btn-sm btn-circle"
              onClick={toggleStatusPanel}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div class="p-4">
          <div class="space-y-4">
            <div class="alert alert-info">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>AI Assistant is ready to help with your career tasks</span>
            </div>
            
            <div class="card bg-base-200">
              <div class="card-body p-4">
                <h3 class="font-bold">Quick Actions</h3>
                <div class="flex flex-wrap gap-2 mt-2">
                  <button class="btn btn-sm btn-outline">New Resume</button>
                  <button class="btn btn-sm btn-outline">Job Search</button>
                  <button class="btn btn-sm btn-outline">Career Advice</button>
                </div>
              </div>
            </div>
            
            <div class="card bg-base-200">
              <div class="card-body p-4">
                <h3 class="font-bold">System Information</h3>
                <div class="text-sm mt-2 space-y-1">
                  <div class="flex justify-between">
                    <span>Version</span>
                    <span class="font-mono">1.0.0</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Status</span>
                    <span class="badge badge-success">Online</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Last Update</span>
                    <span>Just now</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;