// frontend/src/services/AuthService.ts
import { ApiService } from './ApiService';

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
  user: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
  };
  access_token: string;
  token_type: string;
}

export interface RegisterResponse {
  user: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
  };
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

export class AuthService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    return this.apiService.post<LoginResponse>('/auth/login', credentials);
  }

  async register(userData: RegisterData): Promise<RegisterResponse> {
    return this.apiService.post<RegisterResponse>('/auth/register', userData);
  }

  async logout(): Promise<{ message: string }> {
    return this.apiService.post<{ message: string }>('/auth/logout', {});
  }

  async refreshToken(): Promise<RefreshTokenResponse> {
    return this.apiService.post<RefreshTokenResponse>('/auth/refresh', {});
  }
}