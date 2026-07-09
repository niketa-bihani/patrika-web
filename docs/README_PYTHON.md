# Patrika Web QA Automation Framework - Python Edition

A comprehensive QA automation framework built with Playwright and Python for testing the Patrika Web application.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Page Object Model](#page-object-model)
- [Writing Tests](#writing-tests)
- [Configuration](#configuration)
- [Reports](#reports)
- [Best Practices](#best-practices)

## Prerequisites

- Python 3.10+ ([Download](https://www.python.org/downloads/))
- pip (comes with Python)
- Virtual environment (optional but recommended)

## Installation

### 1. Clone or navigate to the project directory
```bash
cd patrika-web
```

### 2. Create a virtual environment (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers
```bash
playwright install
```

### 5. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your test environment details.

## Project Structure

```
patrika-web/
├── pages/
│   ├── __init__.py           # Package initialization
│   ├── base_page.py          # Base class for all pages
│   └── home_page.py          # Home page object
├── tests/
│   ├── __init__.py           # Package initialization
│   └── test_example.py       # Sample test file
├── utils/
│   ├── __init__.py           # Package initialization
│   └── test_helpers.py       # Utility functions and helpers
├── reports/                   # Test reports (generated)
│   ├── screenshots/           # Test failure screenshots
│   └── pytest.log             # Test execution log
├── conftest.py               # Pytest fixtures and configuration
├── pytest.ini                # Pytest configuration
├── pyproject.toml            # Python project configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .env.example              # Environment variables template
├── .mcp.json                 # MCP configuration
└── README.md                 # This file
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run all tests with verbose output
```bash
pytest -v
```

### Run tests in headed mode (see browser)
```bash
pytest --headed
```

### Run tests in debug mode
```bash
pytest --pdb
```

### Run specific test file
```bash
pytest tests/test_example.py
```

### Run specific test class
```bash
pytest tests/test_example.py::TestHomePage
```

### Run specific test function
```bash
pytest tests/test_example.py::TestHomePage::test_navigate_to_home_page
```

### Run tests with specific marker/tag
```bash
# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Critical tests
pytest -m critical
```

### Run tests in parallel (requires pytest-xdist)
```bash
pytest -n auto
```

### Run with custom timeout (in seconds)
```bash
pytest --timeout=60
```

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run tests and generate multiple reports
```bash
pytest --html=reports/report.html --self-contained-html --junit-xml=reports/junit.xml
```

## Page Object Model

The framework uses the Page Object Model pattern for maintainability and reusability.

### Base Page Class

All page objects extend `BasePage` which provides common methods:

```python
from pages.base_page import BasePage
from playwright.async_api import Page

class MyPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    
    async def my_action(self):
        await self.click("selector")
```

### Available Base Methods

- `goto(url)` - Navigate to URL
- `fill_input(selector, text)` - Fill input field
- `click(selector)` - Click element
- `get_text(selector)` - Get element text
- `is_visible(selector)` - Check visibility
- `wait_for_element(selector, timeout)` - Wait for element
- `take_screenshot(filename)` - Capture screenshot
- `get_page_title()` - Get page title
- `get_current_url()` - Get current URL
- `wait_for_load_state(state, timeout)` - Wait for page load state
- `get_attribute(selector, attribute)` - Get element attribute
- `press_key(key)` - Press keyboard key
- `reload()` - Reload page
- `go_back()` - Navigate back
- `go_forward()` - Navigate forward

## Writing Tests

### Basic Test Structure

```python
import pytest
from playwright.async_api import Page
from pages.home_page import HomePage
from utils.test_helpers import log_step

class TestHomePage:
    
    @pytest.fixture
    async def home_page(self, page: Page):
        home_page = HomePage(page)
        yield home_page
    
    @pytest.mark.smoke
    async def test_load_home_page(self, home_page: HomePage):
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()
        
        log_step(2, "Verify header is visible")
        is_visible = await home_page.is_header_visible()
        assert is_visible, "Header should be visible"
```

### Test Naming Conventions

- Use descriptive test names starting with `test_`
- Use lowercase with underscores: `test_user_can_login`
- Use tags for categorization: `@pytest.mark.smoke`, `@pytest.mark.regression`

### Using Test Helpers

```python
from utils.test_helpers import log_step, get_random_email, retry_with_backoff

async def test_example(page):
    log_step(1, "Create account")
    email = get_random_email()
    
    log_step(2, "Retry action if it fails")
    result = await retry_with_backoff(some_async_function, max_retries=3)
```

### Async/Await Pattern

All Playwright operations are async. Use `async` and `await` keywords:

```python
async def test_async_operation(page: Page):
    # Correct
    await page.goto("http://localhost:3000")
    await page.click("button")
    
    # Incorrect - will not work
    page.goto("http://localhost:3000")  # This won't execute properly
```

## Configuration

### pytest.ini

Contains pytest configuration:
- Test discovery patterns
- Async mode (asyncio_mode = auto)
- Test markers/tags
- Output options
- Logging configuration

### conftest.py

Contains pytest fixtures:
- `browser` - Browser instance (session scope)
- `context` - Browser context (function scope)
- `page` - Page object (function scope)
- `base_url` - Application base URL
- `test_timeout` - Test timeout value
- `headless` - Headless mode setting

### Environment Variables (.env)

```
BASE_URL=http://localhost:3000    # Application URL
BROWSER=chromium                   # Browser type
HEADED=false                       # Show browser (true/false)
SLOW_MO=0                         # Slow motion (ms)
TIMEOUT=30000                     # Timeout (ms)
RETRIES=2                         # Retry attempts
DEBUG=false                        # Debug mode
PYTEST_WORKERS=auto              # Parallel workers
```

### pyproject.toml

Modern Python project configuration:
- Project metadata
- Dependencies
- Pytest settings
- Tool configurations (black, isort, mypy)

## Reports

### Generate HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```
View the report: Open `reports/report.html` in your browser

### Generate JUnit XML Report
```bash
pytest --junit-xml=reports/junit.xml
```
Used for CI/CD integration

### View Screenshots
Test failure screenshots are saved to `reports/screenshots/`

### View Test Logs
Test execution logs are saved to `reports/pytest.log`

## Best Practices

### 1. Use Page Objects
Always use page objects instead of hardcoded selectors:
```python
# Good
await home_page.click_logo()

# Avoid
await page.click("a[href='/']")
```

### 2. Descriptive Names
Use clear, descriptive names for tests and methods:
```python
# Good
async def test_user_can_login_with_valid_credentials(self, page):

# Avoid
async def test_login(self, page):
```

### 3. Use Explicit Waits
Use Playwright's built-in waiting mechanisms:
```python
# Good
await page.wait_for_selector("button", timeout=5000)

# Avoid
import time
time.sleep(5)  # Hard sleep
```

### 4. Data Management
Use helpers for test data:
```python
from utils.test_helpers import get_random_email, get_random_string

email = get_random_email()
username = get_random_string(10)
```

### 5. Meaningful Assertions
Keep assertions focused and meaningful:
```python
# Good
is_visible = await home_page.is_header_visible()
assert is_visible, "Header should be visible on home page"

# Avoid
assert await home_page.is_header_visible()
```

### 6. Reusable Helper Methods
Create helpers in BasePage for common actions:
```python
# In BasePage
async def wait_and_click(self, selector: str) -> None:
    await self.wait_for_element(selector)
    await self.click(selector)
```

### 7. Test Markers/Tags
Use markers to organize tests:
```python
@pytest.mark.smoke
@pytest.mark.critical
async def test_important_feature(self, page):
    # Test code
```

### 8. Cleanup
Use pytest fixtures for setup and teardown:
```python
@pytest.fixture
async def setup_user(self, page):
    # Setup
    user = await create_test_user()
    yield user
    # Teardown
    await delete_test_user(user)
```

## Continuous Integration

The framework is CI/CD ready:

### GitHub Actions Example
```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: pytest --junit-xml=reports/junit.xml
```

## Troubleshooting

### Module not found errors
```bash
# Ensure you're in the project directory and virtual environment is activated
pip install -r requirements.txt
```

### Playwright browsers not installed
```bash
playwright install
```

### Tests timeout
- Increase `TIMEOUT` in `.env`
- Check if application is running on configured URL
- Use `pytest --timeout=60` for higher timeout

### Element not found
- Run in headed mode: `pytest --headed`
- Enable debug mode: Set `DEBUG=true` in `.env`
- Use Playwright codegen to record interactions

### Event loop error
- Ensure `asyncio_mode = auto` in `pytest.ini`
- Use `pytest-asyncio` package

### Port already in use
```bash
# Check what's using the port (Windows)
netstat -ano | findstr :3000

# Check what's using the port (macOS/Linux)
lsof -i :3000
```

## Using with MCP (Model Context Protocol)

Your `.mcp.json` is configured with Playwright MCP support:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

This allows integrating with AI coding assistants for test generation and assistance.

## Additional Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Async/Await Guide](https://docs.python.org/3/library/asyncio.html)
- [Best Practices for Test Automation](https://playwright.dev/python/docs/best-practices)

## License

MIT

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Playwright documentation
3. Check pytest documentation
4. Run tests in debug mode: `pytest --pdb`
