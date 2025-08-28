import { test, expect } from '@playwright/test';
import { UserProfilePage } from '../../pages/UserProfilePage';

test('should render the app and display the main title', async ({ page }) => {
  const userProfilePage = new UserProfilePage(page);
  
  // Navigate to the test page
  await userProfilePage.goto();
  
  // Check that the page has the correct title
  const title = await userProfilePage.getTitle();
  expect(title).toMatch(/JobPilot-OpenManus/);
  
  // Check that the profile dashboard is visible
  expect(await userProfilePage.isProfileDashboardVisible()).toBeTruthy();
  
  // Check for the noscript message (which should not be visible when JS is enabled)
  const noScriptElement = page.locator('noscript');
  await expect(noScriptElement).not.toBeVisible();
});