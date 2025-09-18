import type { Component } from 'solid-js';
import { Show } from 'solid-js';
import { Router, Route } from '@solidjs/router';
import { MetaProvider } from '@solidjs/meta';
import { useAuth, AuthProvider } from './contexts/AuthContext';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import { createSignal } from 'solid-js';

// Import our main views
import Header from './components/Header';
import AIChatView from './components/AIChatView';
import JobSearchView from './components/JobSearchView';
import ResumeBuilderView from './components/ResumeBuilderView';

const AppContent: Component = () => {
  const auth = useAuth();
  const [showRegister, setShowRegister] = createSignal(false);

  const handleLoginSuccess = () => {
    // Refresh the auth status
    auth.checkAuthStatus();
  };

  const handleRegisterSuccess = () => {
    // Switch to login form after successful registration
    setShowRegister(false);
  };

  const switchToRegister = () => {
    setShowRegister(true);
  };

  const switchToLogin = () => {
    setShowRegister(false);
  };

  // Render the main app with router
  return (
    <div class="flex flex-col min-h-screen">
      <Router>
        <Route path="/*" component={() => {
          // If not authenticated, show login or register form
          if (!auth.isAuthenticated()) {
            return (
              <div class="flex items-center justify-center min-h-screen bg-base-200">
                {showRegister() ? (
                  <RegisterForm 
                    onRegisterSuccess={handleRegisterSuccess} 
                    onSwitchToLogin={switchToLogin} 
                  />
                ) : (
                  <LoginForm 
                    onLoginSuccess={handleLoginSuccess} 
                    onSwitchToRegister={switchToRegister} 
                  />
                )}
              </div>
            );
          }
          
          // If authenticated, show the main app
          return (
            <>
              <Header />
              <main class="flex-grow mt-16">
                <Route path="/" component={AIChatView} />
                <Route path="/job-search" component={JobSearchView} />
                <Route path="/resume-builder" component={ResumeBuilderView} />
              </main>
            </>
          );
        }} />
      </Router>
    </div>
  );
};

const App: Component = () => {
  return (
    <MetaProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </MetaProvider>
  );
};

export default App;