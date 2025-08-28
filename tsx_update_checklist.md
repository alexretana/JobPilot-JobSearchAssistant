# TSX Component Update Checklist for New Service Layer Integration

## Development Instructions
This checklist outlines the steps required to update the frontend TSX components to integrate with the new service layer using a test-driven approach. The implementation follows a systematic approach:

1. **Set up Playwright testing infrastructure** - Install and configure Playwright for end-to-end testing
2. **Create baseline tests** - Write tests that document current component behavior with mock data
3. **Analyze component dependencies** - Identify which services the component uses (see frontend_update_strategy.md)
4. **Update service imports** - Replace legacy API imports with new service classes
5. **Instantiate services** - Create instances of the new service classes
6. **Adapt component logic** - Modify function calls to match new service interfaces
7. **Implement missing utility functions** - Recreate functionality that was in legacy APIs (see user_profile_update_plan.md)
8. **Update TypeScript types** - Ensure type compatibility with new service definitions
9. **Test functionality with Playwright** - Run tests to verify that component works correctly with new service integration
10. **Update this checklist** after each completed step
11. **Stop after each step** for review

See `frontend_update_strategy.md` for the complete approach and `user_profile_update_plan.md` for detailed implementation guidance.

## Test-Driven Development Approach
Following the Playwright Testing Approach, we'll use a three-phase process:
1. **Phase 1: Baseline Tests** - Create tests that document current component behavior with mock data
2. **Phase 2: Refactoring Tests** - Update components with new service integration and run tests after each change
3. **Phase 3: Validation Tests** - Run complete test suite to verify all functionality including edge cases

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

See `playwright_testing_approach.md` for detailed testing approach and implementation guidelines.
See `frontend/e2e/README.md` for instructions on running tests.
See `frontend/e2e/SETUP_SUMMARY.md` for a summary of what was accomplished.

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
- [ ] Run Playwright tests to verify UserProfile components work correctly
- [ ] Verify UserProfile operations work correctly

### 2. Job Search Components
- [x] Identify all components using `jobApi` imports
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/JobList.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/JobCard.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/JobDetailsModal.tsx`
  - [x] `frontend/src/components/pages/JobSearchPage/JobsTab/SavedJobList.tsx`
- [x] Create baseline Playwright tests for Job Search components
- [ ] Update imports in Job Search components to use `JobService`
- [ ] Instantiate `JobService` in Job Search components
- [ ] Adapt component logic to use `JobService` methods
- [ ] Update TypeScript types to match `JobService` interfaces
- [ ] Run Playwright tests to verify Job Search components work correctly
- [ ] Verify Job Search operations work correctly

### 3. Skill Bank Components
- [ ] Identify all components using `skillBankApi` imports
  - [ ] `frontend/src/components/SkillBankSelectors.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/SkillsSection.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/ExperienceSection.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/EducationSection.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/ProjectsSection.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/SkillBankTab/sections/CertificationsSection.tsx`
- [ ] Create baseline Playwright tests for Skill Bank components
- [ ] Update imports in Skill Bank components to use `SkillBankService`
- [ ] Instantiate `SkillBankService` in Skill Bank components
- [ ] Adapt component logic to use `SkillBankService` methods
- [ ] Update TypeScript types to match `SkillBankService` interfaces
- [ ] Run Playwright tests to verify Skill Bank components work correctly
- [ ] Verify Skill Bank operations work correctly

### 4. Resume Builder Components
- [ ] Identify all components using `resumeApi` imports (if any)
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/ResumeTab/views/ResumeBuilder.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/ResumeTab/views/ResumeList.tsx`
  - [ ] `frontend/src/components/pages/ResumeBuilderPage/ResumeTab/views/ResumePreview.tsx`
- [ ] Create baseline Playwright tests for Resume Builder components
- [ ] Update imports in Resume Builder components to use `ResumeService`
- [ ] Instantiate `ResumeService` in Resume Builder components
- [ ] Adapt component logic to use `ResumeService` methods
- [ ] Update TypeScript types to match `ResumeService` interfaces
- [ ] Run Playwright tests to verify Resume Builder components work correctly
- [ ] Verify Resume Builder operations work correctly

### 5. Timeline Components
- [ ] Identify all components using `timelineApi` imports (if any)
  - [ ] `frontend/src/components/Timeline/TimelineEventCard.tsx`
  - [ ] `frontend/src/components/Timeline/TimelineModal.tsx`
  - [ ] `frontend/src/components/Shared/ActivityLog.tsx`
- [ ] Create baseline Playwright tests for Timeline components
- [ ] Update imports in Timeline components to use `TimelineService`
- [ ] Instantiate `TimelineService` in Timeline components
- [ ] Adapt component logic to use `TimelineService` methods
- [ ] Update TypeScript types to match `TimelineService` interfaces
- [ ] Run Playwright tests to verify Timeline components work correctly
- [ ] Verify Timeline operations work correctly

### 6. Shared and UI Components
- [ ] Identify all components using any legacy API imports
  - [ ] `frontend/src/components/UI/Header.tsx`
  - [ ] `frontend/src/components/UI/StatusPanel.tsx`
- [ ] Create baseline Playwright tests for Shared/UI components
- [ ] Update imports in Shared/UI components to use appropriate services
- [ ] Instantiate required services in Shared/UI components
- [ ] Adapt component logic to use new service methods
- [ ] Update TypeScript types to match service interfaces
- [ ] Run Playwright tests to verify Shared/UI components work correctly
- [ ] Verify Shared/UI operations work correctly

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

## Component Update Validation

### Component Rendering Tests
- [ ] Verify components render with mock data
- [ ] Check that all UI elements are present
- [ ] Confirm proper styling and layout
- [ ] Test responsive design behavior

### User Interaction Tests
- [ ] Test form inputs and validation
- [ ] Verify button clicks and navigation
- [ ] Check that user actions trigger appropriate responses
- [ ] Confirm data updates correctly after user interactions

### Data Flow Tests
- [ ] Verify components receive data correctly from services
- [ ] Check that components display data properly
- [ ] Confirm that user actions update data correctly
- [ ] Test error handling and loading states

### Integration Tests
- [ ] Test complete user workflows
- [ ] Verify data consistency across components
- [ ] Check that components work together correctly
- [ ] Confirm end-to-end functionality

### TypeScript Compatibility
- [ ] Ensure all type definitions match service interfaces
- [ ] Verify no TypeScript compilation errors
- [ ] Confirm type safety in component props and state

### Code Quality
- [ ] Maintain consistent coding style with existing components
- [ ] Ensure components follow Solid.js best practices
- [ ] Verify proper resource cleanup and memory management

## Test Execution

### Development Workflow
- [ ] Run relevant tests during development
- [ ] Use watch mode for continuous testing
- [ ] Run full test suite before committing changes
- [ ] Use test tags for selective test execution

### Continuous Integration
- [ ] Run tests automatically on CI/CD pipeline
- [ ] Generate test reports and coverage metrics
- [ ] Fail builds on test failures
- [ ] Track test performance over time

## Documentation
- [ ] Document Playwright test patterns and conventions
- [ ] Create component update guidelines with testing requirements
- [ ] Document any deviations from standard update process
- [ ] Update component README files if they exist
- [ ] Document test coverage and validation procedures

This checklist ensures comprehensive updating of all TSX components to integrate with the new service layer, providing a clean, consistent frontend architecture without legacy dependencies.