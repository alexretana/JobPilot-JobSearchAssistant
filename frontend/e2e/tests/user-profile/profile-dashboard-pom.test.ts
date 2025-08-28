import { test, expect } from '@playwright/test';
import { UserProfilePage } from '../../pages/UserProfilePage';

test('should render the profile dashboard using page object', async ({ page }) => {
  const userProfilePage = new UserProfilePage(page);
  
  // Navigate to the test page
  await userProfilePage.goto();
  
  // Check that the page has the correct title
  const title = await userProfilePage.getTitle();
  expect(title).toMatch(/JobPilot-OpenManus/);
  
  // Check that the profile dashboard is visible
  expect(await userProfilePage.isProfileDashboardVisible()).toBeTruthy();
  
  // Check that the profile dashboard title is correct
  const profileTitle = await userProfilePage.getProfileTitle();
  expect(profileTitle).toEqual('Profile Dashboard');
  
  // Check that the profile completeness section is visible
  expect(await userProfilePage.isProfileCompletenessVisible()).toBeTruthy();
  
  // Check that the edit profile button is visible
  const editButton = userProfilePage.editProfileButton;
  await expect(editButton).toBeVisible();
  
  // Check that badges are visible in job preferences
  const jobTypeBadges = await userProfilePage.getJobTypeBadges();
  await expect(jobTypeBadges).toHaveCount(1);
  
  const remoteTypeBadges = await userProfilePage.getRemoteTypeBadges();
  await expect(remoteTypeBadges).toHaveCount(2);
  
  const locationBadges = await userProfilePage.getLocationBadges();
  await expect(locationBadges).toHaveCount(3);
});

test('should not show loading or error states using page object', async ({ page }) => {
  const userProfilePage = new UserProfilePage(page);
  
  // Navigate to the test page
  await userProfilePage.goto();
  
  // Check that loading state is hidden
  expect(await userProfilePage.isLoadingStateVisible()).toBeFalsy();
  
  // Check that error state is hidden
  expect(await userProfilePage.isErrorStateVisible()).toBeFalsy();
});