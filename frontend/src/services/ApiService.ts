// frontend/src/services/ApiService.ts

class ApiService {
  private baseUrl = ''; // No /api prefix needed
  private authToken: string | null = null;

  // Set the authentication token
  setAuthToken(token: string | null) {
    this.authToken = token;
  }

  // Get the current authentication token
  getAuthToken(): string | null {
    return this.authToken;
  }

  private async fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    // Prepare headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add authentication header if token exists
    if (this.authToken) {
      headers['Authorization'] = `Bearer ${this.authToken}`;
    }

    const config: RequestInit = {
      headers,
      ...options,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.fetchApi<T>(endpoint, {
      method: 'GET',
    });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.fetchApi<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.fetchApi<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.fetchApi<T>(endpoint, {
      method: 'DELETE',
    });
  }
}

// Export a singleton instance
export const apiService = new ApiService();

// Export the class for those who need to create instances
export default ApiService;