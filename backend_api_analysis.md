# Backend API Analysis

## Overview
The backend API is a comprehensive FastAPI-based system with multiple routers handling different domains of functionality. All endpoints require authentication and are properly structured with appropriate HTTP methods and response models.

## Core API Structure
The API is organized into multiple routers, each handling a specific domain:

### 1. Applications Router (`/applications`)
- **GET /** - List all job applications for the current user with filtering and pagination
- **GET /{application_id}** - Get a specific job application by ID
- **POST /** - Create a new job application
- **PUT /{application_id}** - Update a job application
- **DELETE /{application_id}** - Delete a job application

### 2. Authentication Router (`/auth`)
- **POST /login** - User login
- **POST /register** - User registration
- **POST /logout** - User logout
- **POST /refresh** - Refresh authentication token

### 3. Companies Router (`/companies`)
- **GET /** - List all companies
- **GET /search** - Search companies
- **GET /{company_id}** - Get a specific company
- **POST /** - Create a new company
- **PUT /{company_id}** - Update a company
- **DELETE /{company_id}** - Delete a company
- **GET /{company_id}/jobs** - Get jobs for a specific company

### 4. Job Deduplication Router (`/job-deduplication`)
- **POST /deduplicate** - Deduplicate a single job
- **POST /deduplicate-batch** - Deduplicate a batch of jobs

### 5. Job Sources Router (`/job-sources`)
- **GET /** - List all job sources
- **GET /{source_id}** - Get a specific job source
- **POST /** - Create a new job source
- **PUT /{source_id}** - Update a job source
- **DELETE /{source_id}** - Delete a job source

### 6. Jobs Router (`/jobs`)
- **GET /search** - Search jobs with advanced filtering
- **GET /statistics** - Get job listing statistics
- **GET /** - List all jobs
- **GET /{job_id}** - Get a specific job
- **POST /** - Create a new job
- **PUT /{job_id}** - Update a job
- **DELETE /{job_id}** - Delete a job

### 7. Resumes Router (`/resumes`)
- **GET /** - List all resumes for the current user with filtering and pagination
- **GET /{resume_id}** - Get a specific resume by ID
- **POST /** - Create a new resume
- **PUT /{resume_id}** - Update an existing resume
- **DELETE /{resume_id}** - Delete a resume

### 8. Search Router (`/search`)
- **GET /semantic** - Semantic search
- **GET /hybrid** - Hybrid search

### 9. Skill Banks Router (`/skill-banks`)
- **POST /** - Create a new skill bank for a user
- **GET /{user_id}** - Get a user's skill bank
- **PUT /{user_id}** - Update a user's skill bank
- **DELETE /{user_id}** - Delete a user's skill bank
- **POST /{user_id}/skills** - Add a skill to a user's skill bank
- **PUT /{user_id}/skills/{skill_id}** - Update a skill in a user's skill bank
- **DELETE /{user_id}/skills/{skill_id}** - Delete a skill from a user's skill bank
- **POST /{user_id}/experiences** - Add a work experience to a user's skill bank
- **PUT /{user_id}/experiences/{experience_id}** - Update a work experience in a user's skill bank
- **DELETE /{user_id}/experiences/{experience_id}** - Delete a work experience from a user's skill bank

### 10. Stats Router (`/stats`)
- **GET /general** - General statistics
- **GET /jobs** - Job statistics
- **GET /users** - User statistics
- **GET /applications** - Application statistics
- **GET /resumes** - Resume statistics
- **GET /skill-banks** - Skill bank statistics
- **GET /job-sources** - Job source statistics

### 11. Timeline Router (`/timeline`)
- **GET /** - Get timeline events
- **GET /{event_id}** - Get a specific timeline event
- **POST /** - Create a new timeline event
- **PUT /{event_id}** - Update a timeline event
- **DELETE /{event_id}** - Delete a timeline event

### 12. Users Router (`/users`)
- **GET /search/by-email** - Search users by email
- **GET /default** - Get default user profile (single-user mode)
- **GET /** - List all users
- **GET /{user_id}** - Get a specific user
- **POST /** - Create a new user
- **PUT /{user_id}** - Update a user
- **DELETE /{user_id}** - Delete a user

## Key Features
1. **Authentication**: All endpoints require authentication via `get_current_user` dependency
2. **Authorization**: Users can only access/modify their own data
3. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
4. **Data Validation**: Strong type validation using Pydantic models
5. **Pagination**: Implemented for list endpoints
6. **Filtering**: Rich filtering options for search endpoints
7. **Response Models**: Well-defined response models for all endpoints

## Data Models
The API uses a rich set of data models for different entities:
- Applications
- Companies
- Job sources
- Jobs
- Resumes
- Skill banks (with skills, experiences, education, projects, certifications)
- Timeline events
- Users

## Security
- All endpoints require authentication
- Users can only access their own data
- Proper HTTP status codes for different error conditions
- Input validation and sanitization

This backend API provides a solid foundation for a job search and application tracking system with comprehensive functionality for managing job applications, resumes, skill banks, and user profiles.