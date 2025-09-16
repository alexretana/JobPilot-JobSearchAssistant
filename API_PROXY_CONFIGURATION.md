# API Proxy Configuration Documentation

## Overview
This document explains the proxy configuration used in the Vite development server to enable communication between the frontend (port 3000) and backend (port 8000).

## Why Proxy is Needed
Although both the frontend and backend run on the same host machine, they use different ports:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

Browsers enforce the Same-Origin Policy, which considers different ports as different origins. Without a proxy, API requests from the frontend to the backend would be blocked by CORS restrictions.

## Proxy Configuration

### Current Setup
The proxy is configured in `frontend/vite.config.ts`:

```javascript
proxy: {
  // Proxy all API routes to the backend
  '^/(jobs|users|auth|companies|applications|resumes|skill_banks|timeline|job_sources|search|job_deduplication|stats)/.*': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    secure: false,
  },
  // Also proxy the root-level API endpoints
  '^/(health|test-auth-setting|test-token)$': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    secure: false,
  }
}
```

### How It Works
1. Frontend makes API request to `/jobs/search`
2. Vite intercepts the request (matches the regex pattern)
3. Vite forwards the request to `http://localhost:8000/jobs/search`
4. Backend processes the request and returns the response
5. Vite sends the response back to the frontend
6. Browser receives the response as if it came from `http://localhost:3000`

### Covered Endpoints
The proxy configuration covers all current API endpoints:

- `/jobs/*` - Job listings and search
- `/users/*` - User management
- `/auth/*` - Authentication
- `/companies/*` - Company information
- `/applications/*` - Job applications
- `/resumes/*` - Resume management
- `/skill_banks/*` - Skills management
- `/timeline/*` - Activity timeline
- `/job_sources/*` - Job sources
- `/search/*` - General search
- `/job_deduplication/*` - Job deduplication
- `/stats/*` - Statistics

And root-level endpoints:
- `/health` - Health check
- `/test-auth-setting` - Authentication test
- `/test-token` - Token validation test

## Adding New Endpoints
When adding new API endpoints, update the regex pattern in `vite.config.ts`:

1. If the new endpoint follows the existing pattern (e.g., `/new_feature/*`), add it to the group:
   ```javascript
   '^/(jobs|users|auth|companies|applications|resumes|skill_banks|timeline|job_sources|search|job_deduplication|stats|new_feature)/.*'
   ```

2. If it's a root-level endpoint, add it to the second pattern:
   ```javascript
   '^/(health|test-auth-setting|test-token|new-endpoint)$'
   ```

## Production Considerations
In production, this proxy configuration is not used. Instead, a reverse proxy like nginx typically handles routing:

```
Internet → nginx (port 80/443) → Frontend files (static)
                             → Backend API (proxy to localhost:8000)
```

## Troubleshooting
Common issues and solutions:

1. **API requests still failing**: Verify the regex pattern matches your endpoint
2. **404 errors**: Check that the backend endpoint exists and is correctly configured
3. **Authentication issues**: Ensure auth tokens are being sent correctly
4. **CORS errors in browser console**: Usually indicates the proxy isn't working; restart both servers

## Testing
To verify the proxy is working:
1. Start both frontend and backend servers
2. Navigate to `http://localhost:3000`
3. Open browser developer tools
4. Check the Network tab for API requests
5. Verify requests show `localhost:3000` as the destination but are actually processed by the backend