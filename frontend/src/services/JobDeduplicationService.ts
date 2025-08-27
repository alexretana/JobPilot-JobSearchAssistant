// frontend/src/services/JobDeduplicationService.ts
import { ApiService } from './ApiService';

// Define types for job deduplication
export interface JobForDeduplication {
  id?: string;
  title: string;
  company: string;
  description: string;
  [key: string]: any; // Allow additional properties
}

export interface DeduplicationResult {
  is_duplicate: boolean;
  duplicate_of?: string;
  similarity_score?: number;
}

export interface BatchDeduplicationResult {
  duplicates_found: number;
  duplicate_pairs: Array<{
    job_id_1: string;
    job_id_2: string;
    similarity_score: number;
  }>;
}

export class JobDeduplicationService {
  private apiService: ApiService;

  constructor() {
    this.apiService = new ApiService();
  }

  async deduplicateJob(jobData: JobForDeduplication): Promise<DeduplicationResult> {
    return this.apiService.post<DeduplicationResult>('/job-deduplication/deduplicate', jobData);
  }

  async deduplicateBatch(jobs: JobForDeduplication[]): Promise<BatchDeduplicationResult> {
    return this.apiService.post<BatchDeduplicationResult>('/job-deduplication/deduplicate-batch', { jobs });
  }
}