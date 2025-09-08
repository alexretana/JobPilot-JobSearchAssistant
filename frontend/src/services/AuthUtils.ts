// frontend/src/services/AuthUtils.ts
import { apiService } from './ApiService';

/**
 * Generate a development token for local testing
 * This mimics the backend token structure for development purposes
 */
export const generateDevToken = (userId: string = 'local-dev-user'): string => {
  // Create the payload that matches what the backend expects
  const payload = {
    sub: userId, // User ID
    exp: Math.floor(Date.now() / 1000) + 3600 // Expires in 1 hour
  };
  
  // Encode as the backend does (JSON -> base64)
  const tokenData = JSON.stringify(payload);
  return btoa(tokenData); // Base64 encode
};

/**
 * Initialize authentication for development
 * Sets up a default token for development environments
 */
export const initializeDevAuth = (): void => {
  // Generate and set a development token
  const devToken = generateDevToken('demo-user-123');
  apiService.setAuthToken(devToken);
  
  console.log('Development authentication initialized with token for demo-user-123');
};