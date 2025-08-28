import { Page, Locator } from '@playwright/test';

export class JobSearchPage {
  readonly page: Page;
  readonly jobSearchPage: Locator;
  readonly jobList: Locator;
  readonly jobCards: Locator;
  readonly searchInput: Locator;
  readonly searchButton: Locator;
  readonly loadingState: Locator;
  readonly errorState: Locator;

  constructor(page: Page) {
    this.page = page;
    this.jobSearchPage = page.locator('#job-search-page');
    this.jobList = this.jobSearchPage.locator('.job-list');
    this.jobCards = this.jobList.locator('.job-card');
    this.searchInput = this.jobSearchPage.locator('.search-input');
    this.searchButton = this.jobSearchPage.locator('.search-button');
    this.loadingState = page.locator('#loading-state');
    this.errorState = page.locator('#error-state');
  }

  async goto() {
    await this.page.goto('./test-job-search-page.html');
  }

  async getTitle() {
    return await this.page.title();
  }

  async getJobCardsCount() {
    return await this.jobCards.count();
  }

  async getJobCard(index: number) {
    return this.jobCards.nth(index);
  }

  async searchJobs(query: string) {
    await this.searchInput.fill(query);
    await this.searchButton.click();
  }

  async isLoadingStateVisible() {
    return await this.loadingState.isVisible();
  }

  async isErrorStateVisible() {
    return await this.errorState.isVisible();
  }
}