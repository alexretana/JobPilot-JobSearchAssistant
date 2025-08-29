@echo off
echo Running Playwright tests with automatic server startup...

cd ..
cd frontend
npx playwright test

echo Playwright tests completed.