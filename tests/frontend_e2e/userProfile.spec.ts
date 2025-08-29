import { test, expect } from '@playwright/test';

test.describe('UserProfile Components', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the resume builder page which contains the UserProfileTab
    await page.goto('/');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
  });

  test('should display Profile Dashboard with all sections', async ({ page }) => {
    // Check if the page loaded successfully
    await expect(page).toHaveTitle(/JobPilot/);
    
    // Look for the Profile Dashboard elements
    await expect(page.locator('h1:has-text("Profile Dashboard")')).toBeVisible();
    
    // Check for the three main cards
    await expect(page.locator('h2:has-text("Personal Information")')).toBeVisible();
    await expect(page.locator('h2:has-text("Professional Details")')).toBeVisible();
    await expect(page.locator('h2:has-text("Job Preferences")')).toBeVisible();
    
    // Check for the Edit Profile button
    await expect(page.locator('button:has-text("Edit Profile")')).toBeVisible();
  });

  test('should open Edit Profile modal when Edit Profile button is clicked', async ({ page }) => {
    // Click the Edit Profile button
    await page.click('button:has-text("Edit Profile")');
    
    // Check if the modal is visible
    await expect(page.locator('h3:has-text("Edit Profile")')).toBeVisible();
    
    // Check for form fields in the modal
    await expect(page.locator('input[placeholder="First Name"]')).toBeVisible();
    await expect(page.locator('input[placeholder="Last Name"]')).toBeVisible();
    await expect(page.locator('input[type="email"]')).toBeVisible();
    
    // Close the modal
    await page.click('button:has-text("Cancel")');
  });
});