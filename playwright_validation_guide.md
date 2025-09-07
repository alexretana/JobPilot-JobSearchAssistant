# Playwright MCP Validation for JobPilot Frontend - User Guide

## Overview
This document explains how to use the Playwright MCP validation framework for the JobPilot frontend. The validation process is organized into sections to prevent context overflow and allow focused testing.

## Key Documents
1. [playwright_validation_checklist.md](playwright_validation_checklist.md) - The main checklist for validating frontend components
2. [frontend_components_analysis.md](frontend_components_analysis.md) - Detailed analysis of components and behaviors to validate

## Validation Approach

### Section-by-Section Testing
The validation is organized into sections to manage context tokens effectively:

1. **Section 1**: Core Page Components (Resume Builder Page, Job Search Page)
2. **Section 2**: Resume Builder Tabs (UserProfileTab, ResumeTab, SkillBankTab)
3. **Section 3**: Job Search Tabs (JobsTab, ApplicationsTab, LeadsTab)
4. **Section 4**: Shared Components (ActivityLog)
5. **Section 5**: User Interactions and Workflows
6. **Section 6**: Responsive Design and Cross-Browser Compatibility
7. **Section 7**: Performance and Accessibility

### Run Script Recommendations
Based on our analysis, we recommend using `run_dev_servers.py` as it provides the most robust server management with proper health checks and graceful shutdown capabilities.

## Getting Started

1. **Start the Development Servers**:
   ```bash
   python run_dev_servers.py
   ```

2. **Verify Server Status**:
   - Backend should be accessible at: http://localhost:8000
   - Frontend should be accessible at: http://localhost:3000

3. **Run Playwright Tests via MCP**:
   Instead of using the command line `npx playwright test`, use the Playwright MCP tools directly:
   - Use `browser_navigate` to go to specific pages
   - Use `browser_snapshot` to capture the page structure
   - Use `browser_click` to interact with elements
   - Use `browser_fill_form` to fill in forms
   - Use `browser_take_screenshot` to capture visual states

## Component Validation Process

For each component, validate the following aspects:

1. **Rendering**: Ensure the component loads and displays correctly
2. **Interactions**: Test all user interactions with the component
3. **Data Flow**: Verify data is displayed and updated correctly
4. **Error Handling**: Check how the component handles error conditions
5. **Responsive Design**: Confirm the component works across different viewports
6. **Accessibility**: Validate accessibility features are implemented

## Test Development Guidelines

1. Use the Page Object Model pattern for component interactions
2. Create separate test files for each component or logical group
3. Include both positive and negative test cases
4. Use consistent mock data across tests
5. Generate reports after test runs to track progress

## MCP-Specific Validation Steps

1. **Navigation**: Use `browser_navigate` to go to the target page
2. **Page Analysis**: Use `browser_snapshot` to understand the page structure
3. **Element Interaction**: Use specific MCP tools like `browser_click`, `browser_fill_form`, etc.
4. **State Verification**: Use `browser_snapshot` or `browser_take_screenshot` to verify state changes
5. **Console Monitoring**: Check `browser_console_messages` for any errors

## Next Steps

1. Start with Section 1 of the checklist to validate core page components
2. Proceed through each section sequentially
3. Update the checklist as you complete each validation
4. Refer to the component analysis document for detailed behavior validation requirements
5. Document any issues found during validation