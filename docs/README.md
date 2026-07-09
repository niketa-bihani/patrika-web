# Patrika Web QA Automation Framework

A comprehensive QA automation framework built with Playwright for testing the Patrika Web application.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Page Object Model](#page-object-model)
- [Writing Tests](#writing-tests)
- [Configuration](#configuration)
- [Reports](#reports)

## Prerequisites

- Node.js v18+ ([Download](https://nodejs.org/))
- npm v9+

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd patrika-web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your test environment details

## Project Structure

```
patrika-web/
├── pages/               # Page Object Models
│   ├── BasePage.ts      # Base class for all pages
│   └── HomePage.ts      # Home page object
├── tests/               # Test specifications
│   └── example.spec.ts  # Sample test file
├── utils/               # Utility functions and helpers
│   └── testHelpers.ts   # Common test utilities
├── reports/             # Test reports (generated)
├── playwright.config.ts # Playwright configuration
├── tsconfig.json        # TypeScript configuration
├── package.json         # Project dependencies
└── README.md           # This file
```

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in headed mode (show browser)
```bash
npm run test:headed
```

### Run tests in debug mode
```bash
npm run test:debug
```

### Run tests in UI mode (interactive)
```bash
npm run test:ui
```

### Run tests on specific browser
```bash
npm run test:chrome    # Chromium only
npm run test:firefox   # Firefox only
npm run test:webkit    # WebKit (Safari) only
```

### Run tests on all browsers
```bash
npm run test:all-browsers
```

### Run specific test file
```bash
npx playwright test tests/example.spec.ts
```

### Run tests with specific tag
```bash
npx playwright test --grep @smoke
```

## Page Object Model

The framework uses the Page Object Model pattern for better maintainability and reusability.

### Base Page Class

All page objects extend `BasePage` which provides common methods:

```typescript
import { BasePage } from './BasePage';

export class MyPage extends BasePage {
  readonly mySelector = 'selector';

  async myAction() {
    await this.click(this.mySelector);
  }
}
```

### Available Base Methods

- `goto(url)` - Navigate to URL
- `fillInput(selector, text)` - Fill input field
- `click(selector)` - Click element
- `getText(selector)` - Get element text
- `isVisible(selector)` - Check visibility
- `waitForElement(selector, timeout)` - Wait for element
- `takeScreenshot(filename)` - Screenshot capture
- `getPageTitle()` - Get page title
- `getCurrentUrl()` - Get current URL

## Writing Tests

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/HomePage';

test.describe('Home Page', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
  });

  test('should load home page', async () => {
    await homePage.navigateToHome();
    expect(await homePage.isHeaderVisible()).toBeTruthy();
  });
});
```

### Test Naming Conventions

- Use descriptive test names
- Prefix related tests with group names
- Use tags for categorization: `@smoke`, `@regression`, `@critical`

### Using Test Helpers

```typescript
import { logStep, retryWithBackoff } from '../utils/testHelpers';

test('example test', async () => {
  logStep(1, 'Navigate to page');
  // ...
  
  logStep(2, 'Perform action');
  // ...
});
```

## Configuration

### playwright.config.ts

Key configuration options:

- **testDir**: Directory containing test files
- **fullyParallel**: Run tests in parallel
- **retries**: Number of retries on CI
- **workers**: Number of worker processes
- **reporter**: Test reporters (html, json, junit, list)
- **use.baseURL**: Base URL for tests
- **projects**: Browser configurations

### Environment Variables

Create a `.env` file (use `.env.example` as template):

```env
BASE_URL=http://localhost:3000
BROWSER=chromium
HEADED=false
SLOW_MO=0
TIMEOUT=30000
RETRIES=2
DEBUG=false
```

## Reports

### HTML Report

After test execution, view the HTML report:

```bash
npm run report
```

### Report Formats

- **HTML Report**: `playwright-report/index.html`
- **JSON Report**: `reports/test-results.json`
- **JUnit Report**: `reports/junit.xml`

### Screenshots

Screenshots are automatically saved to `reports/screenshots/` on test failures.

## Best Practices

1. **Use Page Objects**: Always use page objects instead of hardcoded selectors
2. **Descriptive Names**: Use clear, descriptive names for tests and page objects
3. **Waits**: Use explicit waits instead of hard sleeps
4. **Data Management**: Use test helpers for test data generation
5. **Assertions**: Keep assertions focused and meaningful
6. **Reusability**: Create helper methods in BasePage for common actions
7. **Tags**: Use tags to organize tests by type or feature
8. **Cleanup**: Use beforeEach/afterEach for setup and teardown

## Continuous Integration

The framework is CI-ready:

- Tests run sequentially on CI (configurable)
- Automatic retries enabled on CI failures
- Reports generated in standard formats
- Screenshots captured on failures

## Troubleshooting

### Tests timeout
- Increase `timeout` in `playwright.config.ts`
- Check if application is running on configured URL

### Element not found
- Use debug mode: `npm run test:debug`
- Use codegen to record interactions: `npm run codegen`

### Browser crashes
- Run single worker: `npx playwright test --workers=1`
- Clear browser cache and data

## Additional Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Test Guide](https://playwright.dev/docs/intro)
- [Best Practices](https://playwright.dev/docs/best-practices)

## License

MIT
