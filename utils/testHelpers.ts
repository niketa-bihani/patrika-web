import { Page, expect } from '@playwright/test';

/**
 * Common test utilities and helpers
 */

/**
 * Wait for network idle
 */
export async function waitForNetworkIdle(page: Page, timeout: number = 5000): Promise<void> {
  await page.waitForLoadState('networkidle', { timeout });
}

/**
 * Wait for DOM content loaded
 */
export async function waitForDomContentLoaded(page: Page, timeout: number = 5000): Promise<void> {
  await page.waitForLoadState('domcontentloaded', { timeout });
}

/**
 * Retry a function with exponential backoff
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delayMs * Math.pow(2, i)));
    }
  }
  throw new Error('Retry failed');
}

/**
 * Get random string
 */
export function getRandomString(length: number = 10): string {
  return Math.random().toString(36).substring(2, 2 + length);
}

/**
 * Get current timestamp
 */
export function getCurrentTimestamp(): string {
  return new Date().toISOString();
}

/**
 * Log test step
 */
export function logStep(stepNumber: number, stepName: string): void {
  console.log(`\n📍 Step ${stepNumber}: ${stepName}`);
}

/**
 * Generate test report summary
 */
export function generateTestSummary(passed: number, failed: number, skipped: number): void {
  console.log(`
  ╔══════════════════════════════════╗
  ║     TEST EXECUTION SUMMARY       ║
  ╠══════════════════════════════════╣
  ║ ✅ Passed:  ${passed.toString().padStart(24)} ║
  ║ ❌ Failed:  ${failed.toString().padStart(24)} ║
  ║ ⏭️  Skipped: ${skipped.toString().padStart(24)} ║
  ╚══════════════════════════════════╝
  `);
}
