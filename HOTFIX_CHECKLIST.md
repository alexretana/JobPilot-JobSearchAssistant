# HOTFIX CHECKLIST

## Problem Description
The JobSearchView component is failing to load job data from the backend API. The error in the console shows:
```
Error fetching jobs: SyntaxError: Unexpected token '<', "<!doctype " is not valid JSON
```

This indicates that the API call is returning HTML (likely an error page) instead of JSON data.

## Root Cause Analysis
1. The frontend and backend are running on different ports (3000 and 8000), requiring a proxy configuration
2. The API endpoint `/jobs/` requires authentication which wasn't properly configured
3. The API service wasn't handling non-JSON responses properly

## How to Solve It
1. Configure a proxy in Vite to forward API requests from frontend to backend
2. Add proper authentication token handling
3. Improve error handling to distinguish between JSON responses and HTML error pages
4. Use the correct API endpoints for job data

## Leverage context7 mcp tool
Use the context7 mcp tool to:
1. Look up the correct API endpoint structure for the job service
2. Find documentation on how authentication should be implemented
3. Check for any examples of similar API integrations in the codebase
4. Look for backend API documentation to understand the expected response format

## Steps to Implement Fix
1. ✅ Add proxy configuration to vite.config.ts to forward API requests to backend
2. ✅ Update ApiService to handle non-JSON responses gracefully
3. ✅ Update JobService to use the correct endpoints and add better error handling
4. ✅ Update JobSearchView to use searchJobs method instead of listJobs
5. ✅ Add logging to help with debugging API calls
6. ✅ Test the changes by navigating to the Job Search page

## Verification
After implementing the fixes:
1. ✅ The Job Search page loads without errors
2. ✅ Job data is displayed from the backend API
3. ✅ Loading and error states work correctly
4. ✅ Job details modal fetches detailed information from the backend

## Status
✅ **COMPLETED** - All issues have been resolved and functionality has been verified