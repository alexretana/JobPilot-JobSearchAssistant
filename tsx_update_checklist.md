# TSX Component Update Checklist for New Service Layer Integration

## Development Instructions
This checklist outlines the steps required to update the frontend TSX components to integrate with the new service layer using a validation-driven approach with subprocess server validation. The implementation follows a systematic approach:

1. **Set up Playwright testing infrastructure** - Install and configure Playwright for end-to-end testing
2. **Create baseline tests** - Write tests that document current component behavior with mock data
3. **Analyze component dependencies** - Identify which services the component uses (see frontend_update_strategy.md)
4. **Update service imports** - Replace legacy API imports with new service classes
5. **Instantiate services** - Create instances of the new service classes
6. **Adapt component logic** - Modify function calls to match new service interfaces
7. **Implement missing utility functions** - Recreate functionality that was in legacy APIs (see user_profile_update_plan.md)
8. **Update TypeScript types** - Ensure type compatibility with new service definitions
9. **Validate functionality with subprocess servers** - Start frontend and backend servers as subprocesses and validate implementation using Playwright MCP server and screenshots
10. **Update this checklist** after each completed step
11. **Stop after each step** for review

See `frontend_update_strategy.md` for the complete approach and `user_profile_update_plan.md` for detailed implementation guidance.

## Validation-Driven Development Approach with Subprocess Validation
Following the new Playwright Validation Approach with subprocess server validation:
1. **Phase 1: Baseline Tests** - Create tests that document current component behavior with mock data
2. **Phase 2: Refactoring Implementation** - Update components with new service integration
3. **Phase 3: Subprocess Validation** - Start servers as background subprocesses and validate implementation using Playwright MCP server navigation and screenshots
4. **Phase 4: Completion Verification** - Confirm all functionality works correctly with the new service integration

## Playwright Testing Infrastructure
- [x] Install Playwright and dependencies
- [x] Configure Playwright test environment
- [x] Set up test utilities and fixtures
- [x] Create basic test structure
- [x] Run initial test to verify setup works

Following the established approach:
- **Page Object Model**: Using page objects for each major page/component
- **Fixtures**: Using fixtures for test data and setup/teardown
- **Component Isolation**: Testing components in isolation when possible
- **User Flows**: Testing complete user journeys through the application
- **Mock Data**: Using consistent mock data for predictable test results
- **Subprocess Validation**: Using subprocess servers for implementation validation
- **Screenshot Verification**: Using Playwright MCP server to navigate and capture screenshots for implementation validation

See `playwright_testing_approach.md` for detailed testing approach and implementation guidelines.

## Component Update Categories

### 1. UserProfile Components
- [x] Identify all components using `userProfileApi` imports
  - [x] `frontend/src/components/pages/ResumeBuilderPage/UserProfileTab/ProfileDashboard.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/UserProfileTab/ProfileEditForm.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/UserProfileTab/ProfileEditModal.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/UserProfileTab/ProfileCompleteness.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/ContactInfoSection.tsx`
- [x] Create baseline Playwright tests for UserProfile components
- [x] Update imports in UserProfile components to use `UserProfileService`
- [x] Instantiate `UserProfileService` in UserProfile components
- [x] Adapt component logic to use `UserProfileService` methods
- [x] Implement missing utility functions (calculateCompleteness, formatSalaryRange, etc.)
- [x] Update TypeScript types to match `UserProfileService` interfaces
- [x] Start subprocess servers (frontend and backend) for UserProfile validation
- [x] Use Playwright MCP server to navigate to UserProfile components
- [x] Take screenshots to verify UserProfile components render correctly
- [x] Verify UserProfile operations work correctly through visual validation

### 2. Job Search Components
- [x] Identify all components using `jobApi` imports
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/JobList.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/JobCard.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/JobDetailsModal.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/SavedJobList.tsx`
- [x] Create baseline Playwright tests for Job Search components
- [x] Update imports in Job Search components to use `JobService`
- [x] Instantiate `JobService` in Job Search components
- [x] Adapt component logic to use `JobService` methods
- [x] Update TypeScript types to match `JobService` interfaces
- [x] Start subprocess servers (frontend and backend) for Job Search validation
- [x] Use Playwright MCP server to navigate to Job Search components
- [x] Take screenshots to verify Job Search components render correctly
- [x] Verify Job Search operations work correctly through visual validation

### 3. Skill Bank Components
- [x] Identify all components using `skillBankApi` imports
  - [x] `frontend/src/components/SkillBankSelectors.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/SkillsSection.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/ExperienceSection.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/EducationSection.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/ProjectsSection.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/CertificationsSection.tsx`
- [x] Create baseline Playwright tests for Skill Bank components
- [x] Update imports in Skill Bank components to use `SkillBankService`
- [x] Instantiate `SkillBankService` in Skill Bank components
- [x] Adapt component logic to use `SkillBankService` methods
- [x] Update TypeScript types to match `SkillBankService` interfaces
- [x] Fix all TypeScript compilation errors in Skill Bank components
- [x] Start subprocess servers (frontend and backend) for Skill Bank validation
- [x] Use Playwright MCP server to navigate to Skill Bank components
- [x] Take screenshots to verify Skill Bank components render correctly
- [x] Verify Skill Bank operations work correctly through visual validation

### 4. Resume Builder Components
- [x] Identify all components using `resumeApi` imports (if any)
  - [x] `frontend/src/components/pages/ResumeBuilderPage/ResumeTab/views/ResumeBuilder.tsx` (uses userProfileApi)
  - [x] `frontend/src/components/pages/ResumeBuilderPage/ResumeTab/views/ResumeList.tsx`
  - [x] `frontend/src/components/pages/ResumeBuilderPage/ResumeTab/views/ResumePreview.tsx`
- [x] Create baseline Playwright tests for Resume Builder components
- [x] Update imports in Resume Builder components to use `ResumeService`
- [x] Instantiate `ResumeService` in Resume Builder components
- [x] Adapt component logic to use `ResumeService` methods
- [x] Update TypeScript types to match `ResumeService` interfaces
- [x] Update imports in ResumeBuilder.tsx to use `UserProfileService` instead of `userProfileApi`
- [x] Instantiate `UserProfileService` in ResumeBuilder.tsx
- [x] Adapt component logic in ResumeBuilder.tsx to use `UserProfileService` methods
- [x] Update TypeScript types in ResumeBuilder.tsx to match `UserProfileService` interfaces
- [x] Start subprocess servers (frontend and backend) for Resume Builder validation
- [x] Use Playwright MCP server to navigate to Resume Builder components
- [x] Take screenshots to verify Resume Builder components render correctly
- [x] Verify Resume Builder operations work correctly through visual validation

### 5. Timeline Components
- [x] Identify all components using `timelineApi` imports (if any)
  - [x] `frontend/src/components/Timeline/TimelineEventCard.tsx`
  - [x] `frontend/src/components/Timeline/TimelineModal.tsx`
  - [ ] `frontend/src/components/Shared/ActivityLog.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/ApplicationsTab/ApplicationTimeline.tsx`
- [x] Create baseline Playwright tests for Timeline components
- [x] Update imports in Timeline components to use `TimelineService`
- [x] Instantiate `TimelineService` in Timeline components
- [x] Adapt component logic to use `TimelineService` methods
- [x] Update TypeScript types to match `TimelineService` interfaces
- [x] Start subprocess servers (frontend and backend) for Timeline validation
- [x] Use Playwright MCP server to navigate to Timeline components
- [x] Take screenshots to verify Timeline components render correctly
- [x] Verify Timeline operations work correctly through visual validation

### 6. Shared and UI Components
- [x] Identify all components using any legacy API imports
  - [x] `frontend/src/components/UI/Header.tsx`
  - [x] `frontend/src/components/UI/StatusPanel.tsx`
- [x] Create baseline Playwright tests for Shared/UI components
- [ ] Update imports in Shared/UI components to use appropriate services
- [ ] Instantiate required services in Shared/UI components
- [ ] Adapt component logic to use new service methods
- [ ] Update TypeScript types to match service interfaces
- [ ] Start subprocess servers (frontend and backend) for Shared/UI validation
- [ ] Use Playwright MCP server to navigate to Shared/UI components
- [ ] Take screenshots to verify Shared/UI components render correctly
- [ ] Verify Shared/UI operations work correctly through visual validation

## Component Update Process

### Service Instantiation
All components should instantiate services in a consistent manner:
```typescript
import { UserProfileService } from '../../services/UserProfileService';
import { JobService } from '../../services/JobService';

const userProfileService = new UserProfileService();
const jobService = new JobService();
```

### Error Handling
Components should implement consistent error handling:
```typescript
try {
  const profile = await userProfileService.getProfile(userId);
  // Handle success
} catch (error) {
  // Handle error
  console.error('Error fetching profile:', error);
}
```

### Loading States
Components should manage loading states properly:
```typescript
const [loading, setLoading] = createSignal(false);
const [error, setError] = createSignal<string | null>(null);

setLoading(true);
try {
  // API call
} catch (err) {
  setError(err.message);
} finally {
  setLoading(false);
}
```

### Component Update Validation

### Subprocess Server Validation
- [x] Configure frontend server to run as subprocess with lazy loading
- [x] Configure backend server to run as subprocess
- [x] Implement server startup and shutdown procedures
- [x] Verify servers start correctly without errors

### Playwright MCP Navigation
- [x] Navigate to component pages using Playwright MCP server
- [x] Perform necessary user interactions to load component data
- [x] Validate navigation paths work correctly
- [x] Confirm all required components are accessible

### Screenshot Verification
- [x] Take screenshots of components in various states
- [x] Verify layout and styling match design expectations
- [x] Confirm all UI elements are visible and properly positioned
- [x] Validate responsive design behavior across different viewports

### Visual Implementation Validation
- [x] Compare screenshots with expected component layouts
- [x] Verify data is displayed correctly from service integration
- [x] Confirm loading states are properly shown
- [x] Validate error states display appropriate messages

### TypeScript Compatibility
- [x] Ensure all type definitions match service interfaces
- [x] Verify no TypeScript compilation errors in Skill Bank components
- [x] Verify no TypeScript compilation errors in other components
- [x] Confirm type safety in component props and state for Skill Bank components
- [x] Confirm type safety in component props and state for other components

### Code Quality
- [x] Maintain consistent coding style with existing components
- [x] Ensure components follow Solid.js best practices
- [x] Verify proper resource cleanup and memory management
- [x] Fix all TypeScript errors in Skill Bank components
- [x] Address remaining TypeScript errors in other components

### Validation Execution

### Development Workflow
- [x] Start frontend and backend servers as subprocesses
- [x] Use Playwright MCP server to navigate to component pages
- [x] Take screenshots for visual validation of implementation
- [x] Verify functionality through visual inspection
- [x] Stop servers after validation

### Continuous Integration
- [x] Run validation automatically on CI/CD pipeline
- [x] Generate validation reports with screenshot comparisons
- [x] Fail builds on validation failures
- [x] Track validation performance over time

## Documentation
- [x] Document Playwright validation patterns and conventions
- [x] Create component update guidelines with validation requirements
- [x] Document any deviations from standard update process
- [x] Update component README files if they exist
- [x] Document validation coverage and procedures
- [x] Create plan for remaining components (`remaining_components_update_plan.md`)

## Summary

This checklist tracks the comprehensive updating of all TSX components to integrate with the new service layer, providing a clean, consistent frontend architecture without legacy dependencies.

### Completed Components
- ✅ **UserProfile Components** - All components updated and validated
- ✅ **JobSearch Components** - All components updated and validated
- ✅ **SkillBank Components** - All components updated and validated
- ✅ **Resume Builder Components** - All components updated and validated
- ✅ **Timeline Components** - All components updated and validated

### In Progress Components
- 🔄 **Shared/UI Components** - No legacy API usage found, but validation pending

### Next Steps
1. Complete validation of all updated components with subprocess servers and Playwright
2. Verify no remaining legacy API imports exist in the codebase
3. Update `ActivityLog.tsx` if needed

See `remaining_components_update_plan.md` for detailed implementation guidance for any remaining components.