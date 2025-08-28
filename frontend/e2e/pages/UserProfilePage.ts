import { Page, Locator } from '@playwright/test';

export class UserProfilePage {
  readonly page: Page;
  readonly profileDashboard: Locator;
  readonly profileTitle: Locator;
  readonly editProfileButton: Locator;
  readonly profileCompleteness: Locator;
  readonly personalInfoCard: Locator;
  readonly professionalDetailsCard: Locator;
  readonly jobPreferencesCard: Locator;
  readonly loadingState: Locator;
  readonly errorState: Locator;

  constructor(page: Page) {
    this.page = page;
    this.profileDashboard = page.locator('#profile-dashboard');
    this.profileTitle = this.profileDashboard.locator('h2');
    this.editProfileButton = this.profileDashboard.locator('button:has-text("Edit Profile")');
    this.profileCompleteness = this.profileDashboard.locator('.profile-completeness');
    this.personalInfoCard = this.profileDashboard.locator('.card').nth(1);
    this.professionalDetailsCard = this.profileDashboard.locator('.card').nth(2);
    this.jobPreferencesCard = this.profileDashboard.locator('.card').nth(3);
    this.loadingState = page.locator('#loading-state');
    this.errorState = page.locator('#error-state');
  }

  async goto() {
    await this.page.goto('./test-profile-page.html');
  }

  async getTitle() {
    return await this.page.title();
  }

  async getProfileTitle() {
    return await this.profileTitle.textContent();
  }

  async clickEditProfile() {
    await this.editProfileButton.click();
  }

  async isProfileDashboardVisible() {
    return await this.profileDashboard.isVisible();
  }

  async isProfileCompletenessVisible() {
    return await this.profileCompleteness.isVisible();
  }

  async isLoadingStateVisible() {
    return await this.loadingState.isVisible();
  }

  async isErrorStateVisible() {
    return await this.errorState.isVisible();
  }

  async getJobTypeBadges() {
    return this.jobPreferencesCard.locator('.badge-secondary');
  }

  async getRemoteTypeBadges() {
    return this.jobPreferencesCard.locator('.badge-accent');
  }

  async getLocationBadges() {
    return this.jobPreferencesCard.locator('.badge-info');
  }
}