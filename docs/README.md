# Patrika Web QA Automation Framework

A comprehensive QA automation framework built with **Python + Playwright** for testing the Patrika Web application.

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

- Python 3.11+ ([Download](https://www.python.org/))
- pip

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd patrika-web
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

5. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

6. Update `.env` with your test environment details

## Project Structure

```
patrika-web/
├── pages/                # Page Object Models
│   ├── base_page.py      # Base class for all pages
│   ├── home_page.py      # Home page object
│   └── login_page.py     # Login page object
├── tests/                # Test suites
│   └── test_login_from_csv.py  # Login tests (data-driven from CSV)
├── utils/                # Utility functions and helpers
│   ├── csv_loader.py     # CSV test-data loader
│   └── test_helpers.py   # Common test utilities
├── test-data/            # Test data
│   └── LoginTest.csv     # Login test cases
├── reports/              # Test reports (generated)
├── conftest.py           # Pytest fixtures (browser, context, page)
├── pytest.ini            # Pytest configuration
├── pyproject.toml        # Project metadata & dependencies
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run a specific test file
```bash
pytest tests/test_login_from_csv.py -v
```

### Run tests in headed mode (show browser)

Set `HEADED=true` in your `.env` file, then run:
```bash
pytest -v
```

### Run tests by marker (tag)
```bash
pytest -m smoke -v         # Smoke tests only
pytest -m regression -v    # Regression tests only
pytest -m high_priority -v # High-priority tests only
```

### Run a single test by name
```bash
pytest tests/test_login_from_csv.py -k "test_login_modal_displays_correctly" -v
```

## Page Object Model

The framework uses the Page Object Model pattern for better maintainability and reusability.

### Base Page Class

All page objects extend `BasePage`, which provides common methods:

```python
from pages.base_page import BasePage


class MyPage(BasePage):
    MY_SELECTOR = "selector"

    async def my_action(self):
        await self.click(self.MY_SELECTOR)
```

### Available Base Methods

- `goto(url)` — Navigate to URL
- `fill_input(selector, text)` — Fill input field
- `click(selector)` — Click element
- `get_text(selector)` — Get element text
- `is_visible(selector)` — Check visibility
- `wait_for_element(selector, timeout)` — Wait for element
- `take_screenshot(filename)` — Screenshot capture
- `get_page_title()` — Get page title
- `get_current_url()` — Get current URL
- `wait_for_load_state(state, timeout)` — Wait for load state
- `get_attribute(selector, attribute)` — Get element attribute
- `press_key(key)` — Press a keyboard key
- `reload()` / `go_back()` / `go_forward()` — Navigation controls

## Writing Tests

### Basic Test Structure

```python
import pytest
from playwright.async_api import Page
from pages.login_page import LoginPage


class TestLogin:
    @pytest.fixture
    async def login_page(self, page: Page):
        login_page = LoginPage(page)
        await login_page.wait_for_page_load()
        yield login_page

    @pytest.mark.smoke
    async def test_should_open_login(self, login_page: LoginPage):
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        assert await login_page.is_login_modal_visible()
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use markers for categorization: `@pytest.mark.smoke`, `@pytest.mark.regression`, `@pytest.mark.critical`

### Using Test Helpers

```python
from utils.test_helpers import log_step, get_random_string
from utils.csv_loader import CSVDataLoader


async def test_example():
    log_step(1, "Navigate to page")
    # ...

    log_step(2, "Perform action")
    # ...
```

## Configuration

### conftest.py

Defines the core Playwright fixtures:

- **browser** — session-scoped Chromium instance (honors `HEADED` and `SLOW_MO` from `.env`)
- **context** — per-test browser context with `base_url` configured
- **page** — per-test page
- **base_url**, **test_timeout**, **headless** — helper fixtures

### pytest.ini

Key configuration options:

- **testpaths / python_files / python_classes / python_functions** — test discovery rules
- **asyncio_mode** — set to `auto` for async tests
- **addopts** — default CLI options (verbose, HTML report, strict markers)
- **markers** — registered test markers
- **timeout** — per-test timeout guard (via `pytest-timeout`)

### Environment Variables

Create a `.env` file (use `.env.example` as template):

```env
BASE_URL=https://www.patrika.com/
BROWSER=chromium
HEADED=false
SLOW_MO=0
TIMEOUT=30000
RETRIES=2
DEBUG=false
```

## Reports

### HTML Report

A self-contained HTML report is generated automatically after every run at:

```
reports/pytest-report.html
```

### Log File

Execution logs are written to:

```
reports/pytest.log
```

### Screenshots

Use `take_screenshot(filename)` from `BasePage` to capture screenshots during a test.

## Best Practices

1. **Use Page Objects**: Always use page objects instead of hardcoded selectors
2. **Descriptive Names**: Use clear, descriptive names for tests and page objects
3. **Waits**: Use explicit waits instead of hard sleeps
4. **Data Management**: Use `CSVDataLoader` and test helpers for test data
5. **Assertions**: Keep assertions focused and meaningful
6. **Reusability**: Create helper methods in `BasePage` for common actions
7. **Markers**: Use markers to organize tests by type or priority
8. **Fixtures**: Use pytest fixtures for setup and teardown

## Troubleshooting

### Tests timeout
- Increase `timeout` in `pytest.ini`
- Check if the application is reachable at the configured `BASE_URL`

### Element not found
- Run headed to watch the browser: set `HEADED=true` in `.env`
- Use Playwright codegen to record interactions: `playwright codegen https://www.patrika.com`

### Browser issues
- Reinstall browsers: `playwright install`
- Clear browser cache and data

## Additional Resources

- [Playwright for Python](https://playwright.dev/python/)
- [Playwright Python Test Guide](https://playwright.dev/python/docs/intro)
- [pytest Documentation](https://docs.pytest.org/)

## License

MIT
