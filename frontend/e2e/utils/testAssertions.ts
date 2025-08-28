import { Page, Locator } from '@playwright/test';

export class TestAssertions {
  static async assertElementExists(locator: Locator, message?: string) {
    await locator.waitFor({ state: 'visible' });
  }

  static async assertElementNotExists(locator: Locator, message?: string) {
    await locator.waitFor({ state: 'hidden' });
  }

  static async assertTextExists(page: Page, text: string, message?: string) {
    await page.waitForSelector(`text=${text}`);
  }

  static async assertTextNotExists(page: Page, text: string, message?: string) {
    // This is a bit tricky in Playwright, but we can check that the text is not visible
    const elements = await page.$$(text);
    if (elements.length > 0) {
      for (const element of elements) {
        const isVisible = await element.isVisible();
        if (isVisible) {
          throw new Error(message || `Text "${text}" should not be visible`);
        }
      }
    }
  }
}