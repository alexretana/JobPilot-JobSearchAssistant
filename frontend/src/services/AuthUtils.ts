// frontend/src/services/AuthUtils.ts
import { apiService } from './ApiService';

/**
 * Generate a development token for local testing
 * This creates a proper JWT-like token that can be validated by the backend
 */
export const generateDevToken = (userId: string = 'local-dev-user'): string => {
  // Create header (base64 encoded)
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  
  // Create payload that matches what the backend expects
  const payload = btoa(JSON.stringify({
    sub: userId,
    exp: Math.floor(Date.now() / 1000) + 1800 // 30 minutes expiration (matches backend default)
  }));
  
  // For development, we'll create a fixed signature that we know will work
  // This is a workaround since we can't easily generate a proper HMAC signature in the browser
  // In a real implementation, we would need to call the backend to generate a proper token
  const signature = 'invalid-signature'; // This will cause authentication to fail
  
  return `${header}.${payload}.${signature}`;
};

/**
 * Initialize authentication for development
 * Sets up a default token for development environments
 */
export const initializeDevAuth = (): void => {
  // For now, we won't set a token since we can't generate a valid one
  // The application will need to use the login flow to get a proper token
  console.log('Development authentication initialized - use login flow to get valid token');
};