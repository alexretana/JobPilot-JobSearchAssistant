import type { Component } from 'solid-js';
import { Router, Route } from '@solidjs/router';
import { MetaProvider } from '@solidjs/meta';

// Import our main views
import Header from './components/Header';
import AIChatView from './components/AIChatView';
import JobSearchView from './components/JobSearchView';
import ResumeBuilderView from './components/ResumeBuilderView';

const App: Component = () => {
  return (
    <MetaProvider>
      <Router>
        <Route path="/" component={() => (
          <div class="flex flex-col min-h-screen">
            <Header />
            <main class="flex-grow mt-16">
              <AIChatView />
            </main>
          </div>
        )} />
        <Route path="/job-search" component={() => (
          <div class="flex flex-col min-h-screen">
            <Header />
            <main class="flex-grow mt-16">
              <JobSearchView />
            </main>
          </div>
        )} />
        <Route path="/resume-builder" component={() => (
          <div class="flex flex-col min-h-screen">
            <Header />
            <main class="flex-grow mt-16">
              <ResumeBuilderView />
            </main>
          </div>
        )} />
      </Router>
    </MetaProvider>
  );
};

export default App;