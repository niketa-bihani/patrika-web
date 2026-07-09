import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Home Page Object
 * Contains selectors and methods for home page interactions
 */
export class HomePage extends BasePage {
  // Define selectors here
  readonly headerLocator = 'header';
  readonly logoLocator = 'a[href="/"]';
  readonly navigationMenuLocator = 'nav';
  readonly contentLocator = 'main';

  constructor(page: Page) {
    super(page);
  }

  /**
   * Navigate to home page
   */
  async navigateToHome(): Promise<void> {
    await this.goto('/');
  }

  /**
   * Verify header is visible
   */
  async isHeaderVisible(): Promise<boolean> {
    return await this.isVisible(this.headerLocator);
  }

  /**
   * Click on logo to go to home
   */
  async clickLogo(): Promise<void> {
    await this.click(this.logoLocator);
  }

  /**
   * Get header text
   */
  async getHeaderText(): Promise<string | null> {
    return await this.getText(this.headerLocator);
  }
}
