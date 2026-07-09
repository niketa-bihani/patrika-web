import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/HomePage';
import { logStep } from '../utils/testHelpers';

test.describe('Home Page Tests', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
  });

  test('should navigate to home page', async ({ page }) => {
    logStep(1, 'Navigate to home page');
    await homePage.navigateToHome();

    logStep(2, 'Verify page title');
    const title = await homePage.getPageTitle();
    console.log(`Page title: ${title}`);

    logStep(3, 'Verify header is visible');
    const isHeaderVisible = await homePage.isHeaderVisible();
    expect(isHeaderVisible).toBeTruthy();
  });

  test('should have correct URL', async ({ page }) => {
    logStep(1, 'Navigate to home page');
    await homePage.navigateToHome();

    logStep(2, 'Verify current URL');
    const url = await homePage.getCurrentUrl();
    expect(url).toContain('http://localhost:3000');
  });

  test('should click logo and navigate to home', async ({ page }) => {
    logStep(1, 'Navigate to home page');
    await homePage.navigateToHome();

    logStep(2, 'Click on logo');
    await homePage.clickLogo();

    logStep(3, 'Verify navigation');
    const url = await homePage.getCurrentUrl();
    expect(url).toContain('http://localhost:3000');
  });
});
