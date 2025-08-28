# Frontend E2E Tests

This directory contains scripts for running frontend end-to-end tests using Playwright.

## Test Structure
```
tests/
└── frontend_e2e/
    ├── run_e2e_tests.sh      # Unix/Linux/MacOS test runner
    ├── run_e2e_tests.bat     # Windows test runner
    └── README.md             # This file
```

## Test Runner Scripts

### Shell Script (Unix/Linux/MacOS)
```bash
./tests/frontend_e2e/run_e2e_tests.sh
```

### Batch Script (Windows)
```cmd
tests\frontend_e2e\run_e2e_tests.bat
```

## What the Scripts Do

1. **Check Dependencies**: Verify that the frontend directory structure is correct
2. **Install Dependencies**: Install frontend dependencies if node_modules doesn't exist
3. **Install Playwright**: Install Playwright if not already installed
4. **Install Browsers**: Install required browsers for Playwright testing
5. **Run Tests**: Execute the e2e tests using `npm run test:e2e`

## Running Tests

### From Project Root
```bash
# Unix/Linux/MacOS
./tests/frontend_e2e/run_e2e_tests.sh

# Windows
tests\frontend_e2e\run_e2e_tests.bat
```

### Direct Commands
```bash
# Navigate to frontend directory
cd frontend

# Run all e2e tests
npm run test:e2e

# Run e2e tests in UI mode
npm run test:e2e:ui

# Run specific test file
npx playwright test tests/user-profile/profile-dashboard.test.ts
```

## Test Configuration

Tests are configured in `frontend/playwright.config.ts` and organized in `frontend/e2e/` directory.

See `frontend/e2e/README.md` for more detailed information about the test structure and usage.