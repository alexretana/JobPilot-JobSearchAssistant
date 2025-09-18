// frontend/src/services/AuthService.ts
import { apiService } from './ApiService';

// Define types for authentication
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_verified: boolean;
}

export interface RegisterResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_verified: boolean;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

export class AuthService {
  private apiService = apiService;

  constructor() {
    // Load token from localStorage on initialization
    const token = localStorage.getItem('authToken');
    console.log('AuthService constructor called, token from localStorage:', token);
    if (token) {
      this.apiService.setAuthToken(token);
    }
  }

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await this.apiService.post<LoginResponse>('/auth/login', credentials);
    
    // Store the token in the ApiService for future requests
    this.apiService.setAuthToken(response.access_token);
    // Also store in localStorage for persistence
    localStorage.setItem('authToken', response.access_token);
    
    return response;
  }

  async register(userData: RegisterData): Promise<RegisterResponse> {
    return this.apiService.post<RegisterResponse>('/auth/register', userData);
  }

  async logout(): Promise<{ message: string }> {
    const response = await this.apiService.post<{ message: string }>('/auth/logout', {});
    
    // Clear the token from the ApiService
    this.apiService.setAuthToken(null);
    // Also remove from localStorage
    localStorage.removeItem('authToken');
    
    return response;
  }

  async refreshToken(): Promise<RefreshTokenResponse> {
    const response = await this.apiService.post<RefreshTokenResponse>('/auth/refresh', {});
    
    // Update the token in the ApiService
    this.apiService.setAuthToken(response.access_token);
    // Also store in localStorage for persistence
    localStorage.setItem('authToken', response.access_token);
    
    return response;
  }
  
  // Method to set a token manually (useful for development)
  setAuthToken(token: string) {
    this.apiService.setAuthToken(token);
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }
  
  // Method to get the current token
  getAuthToken(): string | null {
    return this.apiService.getAuthToken();
  }
}