# End-to-End Testing with Playwright

## Overview
This directory contains end-to-end tests for the JobPilot-OpenManus frontend application using Playwright. The tests are organized by functionality and follow the Page Object Model pattern for maintainability.

## Test Structure
```
e2e/
├── tests/                    # Test files organized by feature
│   ├── user-profile/        # UserProfile component tests
│   ├── job-search/          # Job search functionality tests
│   ├── skill-bank/          # Skill bank component tests
│   ├── resume-builder/      # Resume builder tests
│   └── shared/              # Shared component tests
├── pages/                   # Page object models
├── components/              # Component object models
├── utils/                   # Utility functions and mock data
├── fixtures/                # Test fixtures
└── test-page.html          # Simple test page for basic tests
```

## Running Tests

### Prerequisites
Make sure you have all dependencies installed:
```bash
npm install
```

### Running All Tests
```bash
npx playwright test
```

### Running Tests for a Specific Feature
```bash
npx playwright test tests/user-profile/
```

### Running a Specific Test File
```bash
npx playwright test tests/user-profile/basic-render.test.ts
```

### Running Tests in a Specific Browser
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Running Tests in UI Mode (Interactive)
```bash
npx playwright test --ui
```

### Running Tests in Debug Mode
```bash
npx playwright test --debug
```

## Writing Tests

### Test Organization
1. Group related tests in the same file
2. Use descriptive test names
3. Follow the AAA pattern (Arrange, Act, Assert)
4. Use page objects for UI interactions
5. Use fixtures for test data

### Example Test Structure
```typescript
import { test, expect } from '@playwright/test';

test('should display user profile information', async ({ page }) => {
  // Arrange
  const userProfilePage = new UserProfilePage(page);
  
  // Act
  await userProfilePage.goto();
  
  // Assert
  await expect(userProfilePage.getTitle()).toHaveText('Profile Dashboard');
});
```

## Page Objects
Page objects encapsulate interactions with specific pages or components. They should:
1. Extend the base Page class
2. Expose methods for common user interactions
3. Return locators for assertions
4. Not contain assertions themselves

### Example Page Object
```typescript
import { Page, Locator } from '@playwright/test';

export class UserProfilePage {
  readonly page: Page;
  readonly title: Locator;
  readonly editButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.locator('h1:text("Profile Dashboard")');
    this.editButton = page.locator('button:text("Edit Profile")');
  }

  async goto() {
    await this.page.goto('/profile');
  }

  async clickEditProfile() {
    await this.editButton.click();
  }
}
```

## Mock Data
Use the mock data utilities in `utils/mockData.ts` to create consistent test data. This ensures tests are deterministic and don't rely on external services.

## Continuous Integration
Tests are automatically run in the CI pipeline. Make sure all tests pass before merging changes.

## Troubleshooting
If tests are failing:
1. Check that all dependencies are installed
2. Verify the test environment is properly configured
3. Run tests in debug mode to see what's happening
4. Check the Playwright documentation for specific issues