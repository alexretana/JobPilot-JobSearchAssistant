// frontend/src/services/CompanyService.ts
import { ApiService } from './ApiService';

// Define types for companies
export interface Company {
  id: string;
  name: string;
  industry?: string;
  website?: string;
  logo_url?: string;
  description?: string;
  [key: string]: any; // Allow additional properties
}

export interface CompanyCreate {
  name: string;
  industry?: string;
  website?: string;
  logo_url?: string;
  description?: string;
}

export interface CompanyUpdate {
  name?: string;
  industry?: string;
  website?: string;
  logo_url?: string;
  description?: string;
}

export interface CompanyListResponse {
  message: string;
  user_id: string;
  companies: Company[];
  total: number;
  page: number;
  page_size: number;
}

export interface CompanySearchResponse {
  message: string;
  user_id: string;
  query: string;
  companies: Company[];
  total: number;
}

export interface CompanyJobsResponse {
  message: string;
  user_id: string;
  company_id: string;
  jobs: any[]; // Job type to be defined later
  total: number;
  page: number;
  page_size: number;
}

export class CompanyService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async listCompanies(limit: number = 20, offset: number = 0): Promise<CompanyListResponse> {
    return this.apiService.get<CompanyListResponse>(`/companies?limit=${limit}&offset=${offset}`);
  }

  async searchCompanies(query: string): Promise<CompanySearchResponse> {
    return this.apiService.get<CompanySearchResponse>(`/companies/search?query=${query}`);
  }

  async getCompany(companyId: string): Promise<Company> {
    return this.apiService.get<Company>(`/companies/${companyId}`);
  }

  async createCompany(companyData: CompanyCreate): Promise<any> {
    return this.apiService.post<any>('/companies', companyData);
  }

  async updateCompany(companyId: string, updateData: CompanyUpdate): Promise<any> {
    return this.apiService.put<any>(`/companies/${companyId}`, updateData);
  }

  async deleteCompany(companyId: string): Promise<any> {
    return this.apiService.delete<any>(`/companies/${companyId}`);
  }

  async getCompanyJobs(companyId: string, limit: number = 20, offset: number = 0): Promise<CompanyJobsResponse> {
    return this.apiService.get<CompanyJobsResponse>(`/companies/${companyId}/jobs?limit=${limit}&offset=${offset}`);
  }
}