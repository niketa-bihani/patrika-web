import { Page, expect } from '@playwright/test';

/**
 * Base Page class that all page objects should extend
 * Provides common utilities for page interactions
 */
export class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  /**
   * Navigate to a specific URL
   */
  async goto(url: string): Promise<void> {
    await this.page.goto(url);
  }

  /**
   * Fill input field with text
   */
  async fillInput(selector: string, text: string): Promise<void> {
    await this.page.fill(selector, text);
  }

  /**
   * Click on an element
   */
  async click(selector: string): Promise<void> {
    await this.page.click(selector);
  }

  /**
   * Get text content of an element
   */
  async getText(selector: string): Promise<string | null> {
    return await this.page.textContent(selector);
  }

  /**
   * Check if element is visible
   */
  async isVisible(selector: string): Promise<boolean> {
    return await this.page.isVisible(selector);
  }

  /**
   * Wait for element to be visible
   */
  async waitForElement(selector: string, timeout: number = 5000): Promise<void> {
    await this.page.waitForSelector(selector, { timeout });
  }

  /**
   * Take a screenshot
   */
  async takeScreenshot(filename: string): Promise<void> {
    await this.page.screenshot({ path: `reports/screenshots/${filename}` });
  }

  /**
   * Get page title
   */
  async getPageTitle(): Promise<string> {
    return await this.page.title();
  }

  /**
   * Get current URL
   */
  async getCurrentUrl(): Promise<string> {
    return this.page.url();
  }
}
