import { test, expect } from '@playwright/test';

test('should render the profile dashboard with all sections', async ({ page }) => {
  // Navigate to the test page
  await page.goto('./test-profile-page.html');
  
  // Check that the page has the correct title
  await expect(page).toHaveTitle(/JobPilot-OpenManus/);
  
  // Check that the root element exists
  await expect(page.locator('#root')).toBeVisible();
  
  // Check that the profile dashboard is visible
  const profileDashboard = page.locator('#profile-dashboard');
  await expect(profileDashboard).toBeVisible();
  
  // Check that the profile dashboard title is correct
  await expect(profileDashboard.locator('h2')).toHaveText('Profile Dashboard');
  
  // Check that the profile completeness section is visible
  const completenessSection = profileDashboard.locator('.profile-completeness');
  await expect(completenessSection).toBeVisible();
  await expect(completenessSection.locator('h3')).toHaveText('Profile Completeness: 75%');
  
  // Check that the edit profile button is visible
  const editButton = profileDashboard.locator('button:has-text("Edit Profile")');
  await expect(editButton).toBeVisible();
  
  // Check that personal information section is visible
  const personalInfoCard = profileDashboard.locator('.card').nth(1);
  await expect(personalInfoCard).toBeVisible();
  await expect(personalInfoCard.locator('h3')).toHaveText('Personal Information');
  
  // Check that professional details section is visible
  const professionalDetailsCard = profileDashboard.locator('.card').nth(2);
  await expect(professionalDetailsCard).toBeVisible();
  await expect(professionalDetailsCard.locator('h3')).toHaveText('Professional Details');
  
  // Check that job preferences section is visible
  const jobPreferencesCard = profileDashboard.locator('.card').nth(3);
  await expect(jobPreferencesCard).toBeVisible();
  await expect(jobPreferencesCard.locator('h3')).toHaveText('Job Preferences');
  
  // Check that badges are visible in job preferences
  const jobTypeBadges = jobPreferencesCard.locator('.badge-secondary');
  await expect(jobTypeBadges).toHaveCount(1);
  
  const remoteTypeBadges = jobPreferencesCard.locator('.badge-accent');
  await expect(remoteTypeBadges).toHaveCount(2);
  
  const locationBadges = jobPreferencesCard.locator('.badge-info');
  await expect(locationBadges).toHaveCount(3);
  
  // Check for the noscript message (which should not be visible when JS is enabled)
  const noScriptElement = page.locator('noscript');
  await expect(noScriptElement).not.toBeVisible();
});

test('should not show loading or error states by default', async ({ page }) => {
  // Navigate to the test page
  await page.goto('./test-profile-page.html');
  
  // Check that loading state is hidden
  const loadingState = page.locator('#loading-state');
  await expect(loadingState).not.toBeVisible();
  
  // Check that error state is hidden
  const errorState = page.locator('#error-state');
  await expect(errorState).not.toBeVisible();
});