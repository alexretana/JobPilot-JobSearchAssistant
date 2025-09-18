import type { Component, JSX } from 'solid-js';
import { createContext, createSignal, useContext } from 'solid-js';
import { AuthService } from '../services/AuthService';

interface AuthContextType {
  isAuthenticated: () => boolean; // Make this a function to access the reactive signal
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuthStatus: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: Component<{ children: JSX.Element }> = (props) => {
  const [isAuthenticated, setIsAuthenticated] = createSignal(false);
  const authService = new AuthService();

  const login = async (email: string, password: string) => {
    try {
      await authService.login({ email, password });
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
      // Still set as logged out even if server call fails
      setIsAuthenticated(false);
    }
  };

  const checkAuthStatus = () => {
    // For now, we'll just check if there's a token
    const token = authService.getAuthToken();
    const authenticated = !!token;
    setIsAuthenticated(authenticated);
    return authenticated;
  };

  // Check auth status on app load
  checkAuthStatus();

  const contextValue: AuthContextType = {
    isAuthenticated, // Pass the signal function directly
    login,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};