import { test, expect } from '@playwright/test';
import { JobSearchPage } from '../../pages/JobSearchPage';

test('should render the job search page with job listings', async ({ page }) => {
  const jobSearchPage = new JobSearchPage(page);
  
  // Navigate to the test page
  await jobSearchPage.goto();
  
  // Check that the page has the correct title
  const title = await jobSearchPage.getTitle();
  expect(title).toMatch(/Job Search/);
  
  // Check that job cards are visible
  const jobCardsCount = await jobSearchPage.getJobCardsCount();
  expect(jobCardsCount).toBe(3);
  
  // Check the first job card
  const firstJobCard = await jobSearchPage.getJobCard(0);
  await expect(firstJobCard.locator('.job-title')).toHaveText('Senior Software Engineer');
  await expect(firstJobCard.locator('.job-company')).toHaveText('Tech Corp');
  
  // Check that badges are visible
  const primaryBadges = firstJobCard.locator('.badge-primary');
  await expect(primaryBadges).toHaveCount(1);
  
  const secondaryBadges = firstJobCard.locator('.badge-secondary');
  await expect(secondaryBadges).toHaveCount(1);
  
  // Check search input and button
  await expect(jobSearchPage.searchInput).toBeVisible();
  await expect(jobSearchPage.searchInput).toHaveValue('Software Engineer');
  await expect(jobSearchPage.searchButton).toBeVisible();
});

test('should not show loading or error states by default', async ({ page }) => {
  const jobSearchPage = new JobSearchPage(page);
  
  // Navigate to the test page
  await jobSearchPage.goto();
  
  // Check that loading state is hidden
  expect(await jobSearchPage.isLoadingStateVisible()).toBeFalsy();
  
  // Check that error state is hidden
  expect(await jobSearchPage.isErrorStateVisible()).toBeFalsy();
});

test('should allow searching for jobs', async ({ page }) => {
  const jobSearchPage = new JobSearchPage(page);
  
  // Navigate to the test page
  await jobSearchPage.goto();
  
  // Perform a search
  await jobSearchPage.searchJobs('Frontend Developer');
  
  // In a real app, this would trigger a navigation or API call
  // For now, we just verify the input was updated
  await expect(jobSearchPage.searchInput).toHaveValue('Frontend Developer');
});