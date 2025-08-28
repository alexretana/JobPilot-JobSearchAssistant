import { Page } from '@playwright/test';

export class AppPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/');
  }

  async getTitle() {
    return await this.page.title();
  }

  getRoot() {
    return this.page.locator('#root');
  }

  getNoScriptMessage() {
    return this.page.locator('noscript');
  }
}