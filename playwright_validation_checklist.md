# Playwright MCP Validation Checklist for Frontend Components

## Overview
This checklist provides a structured approach to validate frontend components using Playwright MCP. The validation is organized by sections to prevent context overflow and allow focused testing.

For a detailed analysis of components and behaviors that need validation, see [frontend_components_analysis.md](frontend_components_analysis.md).

## Prerequisites
Before running any tests, ensure the development servers are running:

### Starting the Servers
Use the recommended approach from the project documentation:

1. **Windows (Recommended):**
   ```cmd
   start_dev_servers.bat
   ```

2. **Cross-Platform Alternative (Python script - most reliable):**
   ```bash
   python run_dev_servers.py
   ```

3. **Cross-Platform Alternative (Batch/Shell scripts):**
   ```bash
   # Windows
   run_all.bat --subprocess
   
   # Linux/Mac
   ./run_all.sh --subprocess
   ```

### Verifying Server Status
After starting the servers, verify they are running:

1. Backend should be accessible at: http://localhost:8000
2. Frontend should be accessible at: http://localhost:3000

You can use these commands to check:
```bash
# Check backend
curl -I http://localhost:8000

# Check frontend
curl -I http://localhost:3000
```

## Section 1: Core Page Components

### Resume Builder Page
- [ ] Navigate to root path ('/')
- [ ] Verify page title contains "JobPilot"
- [ ] Check that the main navigation is visible
- [ ] Verify Resume Builder page loads without errors
- [ ] Confirm page structure includes expected sections

### Job Search Page
- [ ] Navigate to '/jobs' path
- [ ] Verify page title contains "JobPilot"
- [ ] Check that the main navigation is visible
- [ ] Verify Job Search page loads without errors
- [ ] Confirm page structure includes expected sections

## Section 2: Resume Builder Tabs

### UserProfileTab
- [ ] Navigate to Resume Builder page
- [ ] Switch to UserProfileTab
- [ ] Verify UserProfileTab content is displayed
- [ ] Check that user profile form elements are present
- [ ] Test form input interactions
- [ ] Validate form submission (if applicable)

### ResumeTab
- [ ] Navigate to Resume Builder page
- [ ] Switch to ResumeTab
- [ ] Verify ResumeTab content is displayed
- [ ] Check that resume builder elements are present
- [ ] Test resume editing functionality
- [ ] Validate resume save/load functionality (if applicable)

### SkillBankTab
- [ ] Navigate to Resume Builder page
- [ ] Switch to SkillBankTab
- [ ] Verify SkillBankTab content is displayed
- [ ] Check that skill bank elements are present
- [ ] Test skill selection functionality
- [ ] Validate skill addition/removal (if applicable)

## Section 3: Job Search Tabs

### JobsTab
- [ ] Navigate to Job Search page
- [ ] Switch to JobsTab
- [ ] Verify JobsTab content is displayed
- [ ] Check that job listing elements are present
- [ ] Test job search functionality
- [ ] Validate job filtering/sorting (if applicable)

### ApplicationsTab
- [ ] Navigate to Job Search page
- [ ] Switch to ApplicationsTab
- [ ] Verify ApplicationsTab content is displayed
- [ ] Check that applications listing elements are present
- [ ] Test application tracking functionality
- [ ] Validate application status updates (if applicable)

### LeadsTab
- [ ] Navigate to Job Search page
- [ ] Switch to LeadsTab
- [ ] Verify LeadsTab content is displayed
- [ ] Check that leads listing elements are present
- [ ] Test lead tracking functionality
- [ ] Validate lead status updates (if applicable)

## Section 4: Shared Components

### ActivityLog Component
- [ ] Navigate to any page that includes ActivityLog
- [ ] Verify ActivityLog component is displayed
- [ ] Check that activity entries are properly rendered
- [ ] Test activity filtering (if applicable)
- [ ] Validate activity refresh functionality (if applicable)

## Section 5: User Interactions and Workflows

### Navigation Workflow
- [ ] Test main navigation between pages
- [ ] Verify page transitions are smooth
- [ ] Check that user state is maintained across navigation
- [ ] Validate browser back/forward buttons work correctly

### Form Submission Workflow
- [ ] Identify forms in each component
- [ ] Test valid form submissions
- [ ] Validate error handling for invalid inputs
- [ ] Check loading states during submission
- [ ] Verify success/error messages are displayed

### Data Display Workflow
- [ ] Identify data display components
- [ ] Test loading states
- [ ] Validate empty state displays
- [ ] Check error state displays
- [ ] Verify data pagination (if applicable)

## Section 6: Responsive Design and Cross-Browser Compatibility

### Responsive Design
- [ ] Test layout on mobile viewport (375x667)
- [ ] Test layout on tablet viewport (768x1024)
- [ ] Test layout on desktop viewport (1280x800)
- [ ] Verify components adapt to different screen sizes
- [ ] Check that touch interactions work on mobile

### Browser Compatibility
- [ ] Test in Chromium (default)
- [ ] Test in Firefox
- [ ] Test in WebKit (Safari)
- [ ] Verify consistent behavior across browsers
- [ ] Check for browser-specific rendering issues

## Section 7: Performance and Accessibility

### Performance Metrics
- [ ] Measure page load times
- [ ] Test time to interactive
- [ ] Validate bundle sizes don't cause delays
- [ ] Check for memory leaks during navigation
- [ ] Verify API response times are acceptable

### Accessibility
- [ ] Test keyboard navigation
- [ ] Verify proper focus management
- [ ] Check ARIA attributes are correctly applied
- [ ] Validate color contrast ratios
- [ ] Test screen reader compatibility

## Running Playwright Tests

### Test Execution Commands
```bash
# Run all tests
cd frontend && npx playwright test

# Run tests for a specific section
cd frontend && npx playwright test tests/resume-builder/

# Run tests in headed mode
cd frontend && npx playwright test --headed

# Run tests with trace viewer
cd frontend && npx playwright test --trace on

# Run tests with UI mode
cd frontend && npx playwright test --ui
```

### Environment Setup
1. Ensure all dependencies are installed:
   ```bash
   cd frontend && npm install
   ```

2. Install Playwright browsers (if not already installed):
   ```bash
   cd frontend && npx playwright install
   ```

3. Verify Playwright installation:
   ```bash
   cd frontend && npx playwright test --version
   ```

## Test Development Guidelines

### Test Structure
1. Use Page Object Model for component interactions
2. Create separate test files for each component
3. Group related tests in describe blocks
4. Use meaningful test descriptions
5. Include both positive and negative test cases

### Mock Data Strategy
1. Create consistent mock data for predictable tests
2. Use different data scenarios (empty, partial, complete)
3. Include error scenarios and edge cases
4. Maintain mock data consistency across tests

### Reporting
1. Generate HTML reports after test runs
2. Capture screenshots on test failures
3. Record videos for complex interactions
4. Track test execution times
5. Monitor test coverage metrics

## Validation Completion Criteria

### For Each Section:
- [ ] All tests pass without failures
- [ ] No console errors during test execution
- [ ] All critical user workflows function correctly
- [ ] Responsive design works across viewport sizes
- [ ] Performance metrics meet acceptable thresholds
- [ ] Accessibility standards are maintained

### Overall Validation:
- [ ] All sections have been validated
- [ ] Cross-browser compatibility confirmed
- [ ] Test coverage metrics are acceptable
- [ ] No critical or high-severity issues found
- [ ] Documentation updated with test results

## Run Script Analysis and Recommendations

### Script Quality Assessment

#### Good Scripts (Recommended for Use):
1. **run_dev_servers.py** - Most robust implementation with:
   - Proper process management
   - Health checks using actual HTTP requests
   - Graceful shutdown with signal handlers
   - Error handling for process failures
   - Cross-platform compatibility
   - Clear status feedback

2. **run_all.bat / run_all.sh** - Good cross-platform scripts with:
   - Support for both foreground and subprocess modes
   - Proper cleanup mechanisms for subprocesses
   - Signal handlers in shell version for graceful shutdown

3. **start_dev_servers.bat / stop_dev_servers.bat** - Functional Windows-specific scripts:
   - Simple and direct approach for Windows users
   - Basic health checks
   - Clear user instructions

#### Scripts with Limitations:
1. **start_dev_servers.bat** - Has a fixed 15-second timeout which might not be enough for slower machines
2. **stop_dev_servers.bat** - Relies on window titles which may not be reliable if they change

### Recommendations for Server Startup in Playwright Testing

1. **Primary Recommendation**: Use `run_dev_servers.py` for the most reliable server management during testing
2. **Windows Alternative**: Use `start_dev_servers.bat` for quick Windows-based testing
3. **Cross-Platform Alternative**: Use `run_all.bat --subprocess` or `./run_all.sh --subprocess` for cross-platform compatibility
4. **Validation Process**: Always verify servers are running before executing Playwright tests by checking HTTP responses from both backend (port 8000) and frontend (port 3000)