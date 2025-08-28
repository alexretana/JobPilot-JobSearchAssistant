// Utility functions for component updates
// This file contains helper functions that will be used during the component refactoring process

/**
 * Format salary range for display
 * @param min Minimum salary
 * @param max Maximum salary
 * @returns Formatted salary range string
 */
export function formatSalaryRange(min?: number, max?: number): string {
  if (!min && !max) {
    return 'Salary not specified';
  }

  if (min && max) {
    return `$${min.toLocaleString()} - $${max.toLocaleString()}`;
  }

  if (min) {
    return `$${min.toLocaleString()}+`;
  }

  if (max) {
    return `Up to $${max.toLocaleString()}`;
  }

  return 'Salary not specified';
}

/**
 * Format posted date for display
 * @param postedDate Posted date string
 * @returns Formatted date string
 */
export function formatPostedDate(postedDate: string | null): string {
  if (!postedDate) {
    return 'Date not specified';
  }

  const date = new Date(postedDate);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 1) {
    return '1 day ago';
  } else if (diffDays < 7) {
    return `${diffDays} days ago`;
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7);
    return weeks === 1 ? '1 week ago' : `${weeks} weeks ago`;
  } else {
    return date.toLocaleDateString();
  }
}

/**
 * Get job type display label
 * @param jobType Job type string
 * @returns Display label for job type
 */
export function getJobTypeLabel(jobType: string | null): string {
  if (!jobType) return 'Not specified';

  const labels: Record<string, string> = {
    'Full-time': 'Full-time',
    'Part-time': 'Part-time',
    Contract: 'Contract',
    Temporary: 'Temporary',
    Internship: 'Internship',
    Volunteer: 'Volunteer',
  };

  return labels[jobType] || jobType;
}

/**
 * Get remote type display label
 * @param remoteType Remote type string
 * @returns Display label for remote type
 */
export function getRemoteTypeLabel(remoteType: string | null): string {
  if (!remoteType) return 'Not specified';

  const labels: Record<string, string> = {
    Remote: 'Remote',
    'On-site': 'On-site',
    Hybrid: 'Hybrid',
  };

  return labels[remoteType] || remoteType;
}

/**
 * Get remote type icon
 * @param remoteType Remote type string
 * @returns Icon for remote type
 */
export function getRemoteTypeIcon(remoteType: string | null): string {
  const icons: Record<string, string> = {
    Remote: '🏠',
    'On-site': '🏢',
    Hybrid: '🔄',
  };

  return icons[remoteType || ''] || '📍';
}

/**
 * Calculate profile completeness
 * @param profile User profile object
 * @returns Completeness data
 */
export function calculateProfileCompleteness(profile: any): any {
  // This is a simplified implementation
  // In a real implementation, this would calculate based on actual profile fields
  const sections = {
    personal: profile.first_name && profile.last_name && profile.email ? 100 : 50,
    professional: profile.current_title && profile.experience_years ? 100 : 50,
    preferences: profile.preferred_job_types && profile.preferred_job_types.length > 0 ? 100 : 50,
  };

  const overallScore = Math.round(
    (sections.personal + sections.professional + sections.preferences) / 3
  );

  return {
    overall_score: overallScore,
    sections,
    missing_fields: [],
    suggestions: [],
  };
}

/**
 * Validate profile data
 * @param profile Profile data to validate
 * @returns Array of validation errors
 */
export function validateProfile(profile: any): string[] {
  const errors: string[] = [];

  if (!profile.last_name) {
    errors.push('Last name is required');
  }

  if (!profile.email) {
    errors.push('Email is required');
  }

  if (profile.skills && profile.skills.length === 0) {
    errors.push('At least one skill is required');
  }

  if (profile.preferred_job_types && profile.preferred_job_types.length === 0) {
    errors.push('At least one preferred job type is required');
  }

  if (profile.preferred_remote_types && profile.preferred_remote_types.length === 0) {
    errors.push('At least one preferred remote type is required');
  }

  return errors;
}

/**
 * Get job types
 * @returns Array of job types
 */
export function getJobTypes(): string[] {
  return ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Volunteer'];
}

/**
 * Get remote types
 * @returns Array of remote types
 */
export function getRemoteTypes(): string[] {
  return ['On-site', 'Remote', 'Hybrid'];
}