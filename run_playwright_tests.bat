@echo off
echo Running Playwright tests with automatic server startup...

cd frontend
npx playwright test

echo Playwright tests completed.