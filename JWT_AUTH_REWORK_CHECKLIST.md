# JWT Authentication Rework Checklist

## Design Decisions

### 1. Core Architecture
- **Authentication Method**: JWT (JSON Web Tokens) with cryptographic signing
- **Token Type**: Access tokens only (no refresh tokens in initial implementation)
- **Signing Algorithm**: HS256 (HMAC with SHA-256)
- **Token Expiration**: 30 minutes (configurable via settings)
- **Storage**: LocalStorage on frontend, HttpOnly cookies for future enhancement

### 2. Database Changes
- **User Model**: Extend existing `UserProfileDB` with authentication fields
- **New Fields**:
  - `hashed_password`: VARCHAR(128) for securely stored passwords
  - `is_active`: BOOLEAN for account status
  - `is_verified`: BOOLEAN for email verification status
  - `last_login`: DATETIME for tracking user activity
- **Constraints**:
  - Add unique constraint on email field
  - Add validation for password strength

### 3. Security Considerations
- **Password Hashing**: Use bcrypt with appropriate work factor
- **Token Security**: Cryptographically signed JWT tokens
- **CORS**: Proper CORS configuration to prevent unauthorized access
- **Rate Limiting**: Implement rate limiting on authentication endpoints
- **Input Validation**: Strict validation on all authentication inputs

### 4. Backend Implementation
- **Dependencies**: Add `PyJWT` and `bcrypt` to backend requirements
- **Endpoints**:
  - `/auth/login`: Authenticate user and return JWT token
  - `/auth/register`: Create new user account
  - `/auth/logout`: Client-side token invalidation (server-side in future)
  - `/auth/refresh`: Token refresh mechanism (future enhancement)
  - `/auth/verify`: Email verification endpoint (future enhancement)
- **Middleware**: Update authentication middleware to validate JWT tokens

### 5. Frontend Implementation
- **Token Storage**: localStorage for token persistence
- **Token Handling**: Automatic inclusion of Authorization header
- **Token Refresh**: Silent token refresh before expiration
- **Protected Routes**: Guard routes that require authentication
- **User Context**: Global user state management

### 6. Development vs Production
- **Environment Configuration**: Use environment variables for secrets
- **Development Mode**: Allow easier testing with debug logging
- **Production Security**: Enforce stricter security measures

## Development Instructions

### 1. Backend Development

#### Step 1: Add Dependencies
```bash
# Add to pyproject.toml
pyjwt>=2.8.0
bcrypt>=4.1.0
```

#### Step 2: Update User Model
1. Modify `UserProfileDB` in `backend/data/models.py` to add authentication fields
2. Add database migration to update existing tables

#### Step 3: Implement JWT Utilities
1. Update `backend/api/auth.py` with proper JWT token creation/validation
2. Add password hashing functions using bcrypt

#### Step 4: Update Authentication Endpoints
1. Modify `backend/api/routers/auth.py` with real authentication logic
2. Implement proper user registration with email uniqueness check
3. Implement proper login with password verification

#### Step 5: Update Authentication Middleware
1. Update `get_current_user` function to properly validate JWT tokens
2. Ensure all protected endpoints require valid JWT tokens

### 2. Frontend Development

#### Step 1: Update Authentication Service
1. Modify `frontend/src/services/AuthService.ts` to handle real JWT tokens
2. Implement proper error handling for authentication failures

#### Step 2: Update API Service
1. Ensure `frontend/src/services/ApiService.ts` properly handles JWT tokens
2. Implement automatic token refresh mechanism

#### Step 3: Implement Protected Routes
1. Add route guards to protect authenticated-only routes
2. Implement redirect logic for authentication flow

#### Step 4: Update User Context
1. Implement global user state management
2. Ensure UI updates properly based on authentication status

### 3. Testing

#### Step 1: Unit Tests
1. Write unit tests for authentication utilities
2. Test password hashing and verification
3. Test JWT token creation and validation

#### Step 2: Integration Tests
1. Test authentication endpoints with real database
2. Test protected endpoints with valid/invalid tokens
3. Test edge cases and error conditions

#### Step 3: End-to-End Tests
1. Test complete authentication flow in browser
2. Test protected route access
3. Test token expiration and refresh

## Implementation Checklist

### Backend Tasks
- [ ] Add PyJWT and bcrypt dependencies to pyproject.toml
- [ ] Update UserProfileDB model with authentication fields
- [ ] Add database migration for new user fields
- [ ] Implement password hashing utility functions
- [ ] Implement JWT token creation and validation functions
- [ ] Update authentication router with real implementation
- [ ] Implement user registration with email uniqueness check
- [ ] Implement user login with password verification
- [ ] Update authentication middleware to validate JWT tokens
- [ ] Add proper error handling and HTTP status codes
- [ ] Implement rate limiting on authentication endpoints
- [ ] Add logging for authentication events
- [ ] Update configuration to use secure secret key
- [ ] Write unit tests for authentication utilities
- [ ] Write integration tests for authentication endpoints
- [ ] Update documentation for new authentication system

### Frontend Tasks
- [ ] Update AuthService to handle real JWT tokens
- [ ] Implement proper error handling for authentication failures
- [ ] Update ApiService to properly handle JWT tokens
- [ ] Implement automatic token refresh mechanism
- [ ] Add route guards for protected routes
- [ ] Implement authentication flow redirect logic
- [ ] Implement global user state management
- [ ] Update UI to reflect authentication status
- [ ] Add loading states during authentication
- [ ] Implement logout functionality
- [ ] Write unit tests for authentication service
- [ ] Write integration tests for authentication flow
- [ ] Update documentation for frontend authentication

### Database Tasks
- [ ] Add hashed_password field to UserProfileDB
- [ ] Add is_active field to UserProfileDB
- [ ] Add is_verified field to UserProfileDB
- [ ] Add last_login field to UserProfileDB
- [ ] Add unique constraint on email field
- [ ] Add validation constraints for password fields
- [ ] Create database migration script
- [ ] Test migration with existing data
- [ ] Update database documentation

### Security Tasks
- [ ] Implement password strength validation
- [ ] Add rate limiting to authentication endpoints
- [ ] Implement secure token storage (HttpOnly cookies for future)
- [ ] Add CORS configuration for authentication endpoints
- [ ] Implement input validation for all authentication inputs
- [ ] Add security headers to API responses
- [ ] Implement proper error messages that don't leak information
- [ ] Add logging for security events
- [ ] Perform security audit of authentication implementation

### Testing Tasks
- [ ] Write unit tests for backend authentication utilities
- [ ] Write unit tests for frontend authentication service
- [ ] Write integration tests for authentication endpoints
- [ ] Write integration tests for protected endpoints
- [ ] Write end-to-end tests for authentication flow
- [ ] Write tests for error conditions and edge cases
- [ ] Perform load testing on authentication endpoints
- [ ] Test token expiration and refresh scenarios
- [ ] Test concurrent login scenarios
- [ ] Test account lockout scenarios (future enhancement)

### Documentation Tasks
- [ ] Update API documentation for authentication endpoints
- [ ] Update frontend documentation for authentication service
- [ ] Create developer guide for authentication system
- [ ] Create user guide for authentication features
- [ ] Document environment configuration for authentication
- [ ] Document security considerations and best practices
- [ ] Update README with authentication setup instructions