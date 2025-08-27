# Frontend Services Layer Analysis

## Overview
The frontend services layer consists of several TypeScript service classes that handle communication with the backend API. These services are primarily focused on making HTTP requests and processing responses, without handling UI rendering logic.

## Current Service Files

### 1. ApiService (`api.ts`)
A basic service for generic API calls:
- Health check endpoint
- Job search functionality
- Chat history retrieval

**Issues**:
- Very limited functionality compared to backend API
- Hardcoded API base URL (`/api`)
- Basic error handling

### 2. JobApiService (`jobApi.ts`)
Handles job-related API interactions:
- Get recent jobs
- Get detailed job information
- Search jobs with filters
- Helper methods for formatting job data (salary, dates, etc.)
- Saved jobs functionality (save/unsave jobs, check if saved, etc.)

**Issues**:
- Uses `window.location.origin` instead of consistent API base URL
- Missing many job endpoints available in backend (statistics, CRUD operations)
- Saved jobs functionality endpoints don't match backend API structure

### 3. SkillBankApiService (`skillBankApi.ts`)
Handles skill bank operations:
- Get user's complete skill bank
- Update skill bank information
- Skills management (add, get, update, delete)
- Summary variations
- Experience management
- Education management
- Projects management
- Certifications management
- Data migration
- Utility operations (categories, statistics)

**Issues**:
- Hardcoded API base URL (`/api/skill-bank`) that doesn't match backend (`/skill-banks`)
- Some endpoints may not match current backend implementation exactly

### 4. TimelineApiService (`timelineApi.ts`)
Handles timeline events:
- User timeline retrieval with filtering options
- User milestones
- Upcoming events
- Job and application timelines
- Event management (create, update, delete)
- Convenience methods for logging specific events
- Utility methods

**Issues**:
- Hardcoded API base URL (`/api/timeline`) that may not match backend
- May be missing some backend endpoints

### 5. UserProfileApiService (`userProfileApi.ts`)
Handles user profile operations:
- Create, get, update, delete user profiles
- List profiles with pagination
- Search by email
- Profile completeness calculation
- Validation helpers

**Issues**:
- Uses `window.location.origin` instead of consistent API base URL
- Some endpoints don't match backend API structure exactly

### 6. ResumeService (`resumeService.ts`)
Handles resume operations:
- Get user resumes
- Get specific resume
- Create, update, delete resumes
- Export resumes in various formats
- Resume analytics
- Template management
- AI-generated resume content

**Issues**:
- Hardcoded API base URL (`http://localhost:8080`) which is incorrect
- Some endpoints don't match backend API structure exactly
- Missing some backend endpoints

### 7. ResumeImportService (`resumeImportService.ts`)
Handles mapping user profile data to resume structure:
- Map profile to resume
- Create import preview
- Validate profile for import

**Issues**:
- Depends on potentially outdated UserProfile structure
- May not align with current Skill Bank implementation

### 8. WebSocketService (`websocket.ts`)
Handles WebSocket connections:
- Connect/disconnect
- Send messages
- Message handling
- Reconnection logic

**Issues**:
- Hardcoded WebSocket URL (`ws://${window.location.hostname}:8080/ws`)
- May not match backend WebSocket implementation

## Major Issues

### 1. Inconsistent API Base URLs
Services use different approaches for API base URLs:
- Hardcoded paths (`/api/skill-bank`)
- Window origin (`window.location.origin`)
- Hardcoded development URLs (`http://localhost:8080`)

### 2. Missing Functionality
Many backend endpoints are not implemented in the frontend services:
- Job statistics
- Job CRUD operations
- Company endpoints
- Job source endpoints
- Search endpoints (semantic, hybrid)
- Stats endpoints
- Auth endpoints
- Application endpoints

### 3. Endpoint Mismatches
Some frontend service endpoints don't match the backend API structure:
- Saved jobs functionality
- Resume endpoints
- Skill bank endpoints

### 4. Outdated Patterns
- Some services use class-based singleton patterns, others don't
- Inconsistent error handling approaches
- Mixed use of async/await and Promise patterns

## Recommendations

### 1. Complete Rewrite (Recommended)
Given the extensive mismatches between frontend services and backend API, a complete rewrite would be most efficient:
- Create a unified API service with consistent base URL handling
- Implement all backend endpoints
- Standardize error handling
- Use consistent patterns across all services

### 2. Incremental Update
If time is constrained, prioritize updating services based on frontend requirements:
- UserProfileApiService and SkillBankApiService (core user functionality)
- JobApiService (job search is likely a primary feature)
- ResumeService (resume management is important)
- AuthenticationService (if separate from UserProfile)