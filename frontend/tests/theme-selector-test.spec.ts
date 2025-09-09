import { test, expect } from '@playwright/test';

test('theme selector behavior', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Wait for the page to load
  await page.waitForLoadState('networkidle');
  
  // Find the theme selector element (assuming it's a select element or has specific data-testid)
  // We'll try multiple common selectors for theme pickers
  const themeSelector = await page.locator('[data-testid="theme-selector"], #theme-selector, .theme-selector, select');
  const themeButton = await page.locator('button:has-text("Theme"), button:has-text("theme")');
  
  console.log('Looking for theme selector elements...');
  
  if (await themeSelector.count() > 0) {
    console.log('Found theme selector element');
    // Log the element's HTML
    console.log(await themeSelector.first().innerHTML());
  } else if (await themeButton.count() > 0) {
    console.log('Found theme button element');
    // Click the theme button to reveal options
    await themeButton.first().click();
    // Wait a bit for any dropdown to appear
    await page.waitForTimeout(500);
  } else {
    // Try to find any element that might be related to themes
    const possibleThemeElements = await page.locator('[class*="theme"], [id*="theme"], [data-*="theme"]').all();
    console.log(`Found ${possibleThemeElements.length} possible theme-related elements`);
    
    for (let i = 0; i < Math.min(3, possibleThemeElements.length); i++) {
      console.log(`Element ${i}:`, await possibleThemeElements[i].innerHTML());
    }
  }
  
  // Try to find and test different theme options
  // Look for all buttons or options that might represent themes
  const themeOptions = await page.locator('button, [role="option"], .theme-option').all();
  console.log(`Found ${themeOptions.length} possible theme options`);
  
  // Log information about the body element's classes to see current theme
  const bodyClasses = await page.locator('body').getAttribute('class');
  console.log(`Current body classes: ${bodyClasses}`);
  
  // Try to find DaisyUI theme classes
  const htmlClasses = await page.locator('html').getAttribute('class');
  console.log(`Current html classes: ${htmlClasses}`);
});