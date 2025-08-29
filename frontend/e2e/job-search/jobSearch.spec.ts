import { test, expect } from '@playwright/test';

test.describe('Job Search Components', () => {
  test('should load job search page', async ({ page }) => {
    // Navigate to the job search page
    await page.goto('/jobs');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check if the page loaded successfully
    await expect(page).toHaveTitle(/JobPilot/);
  });

  test('should load resume builder page', async ({ page }) => {
    // Navigate to the resume builder page
    await page.goto('/');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check if the page loaded successfully
    await expect(page).toHaveTitle(/JobPilot/);
  });
});