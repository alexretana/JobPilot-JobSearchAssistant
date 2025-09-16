import type { Component } from 'solid-js';
import { A } from '@solidjs/router';

const Header: Component = () => {
  const themes = [
    'light',
    'dark',
    'retro',
    'cyberpunk',
    'valentine',
    'aqua'
  ];

  const handleThemeChange = (theme: string) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
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

          {/* Right side - Theme Selector */}
          <div class="dropdown dropdown-end">
            <div tabindex={0} role="button" class="btn btn-ghost btn-sm">
              Theme
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            <ul tabindex={0} class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52 mt-1">
              {themes.map((theme) => (
                <li>
                  <a onClick={() => handleThemeChange(theme)}>{theme.charAt(0).toUpperCase() + theme.slice(1)}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;