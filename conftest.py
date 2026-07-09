"""
Pytest Configuration and Fixtures
Contains fixtures and configuration for pytest and Playwright.
"""

import pytest
import os
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
async def browser():
    """
    Fixture to provide a browser instance for the test session.
    
    Yields:
        Playwright Browser object
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()


@pytest.fixture
async def context(browser: Browser) -> BrowserContext:
    """
    Fixture to provide a new browser context for each test.
    
    Args:
        browser: Browser instance from session fixture
        
    Yields:
        Playwright BrowserContext object
    """
    context = await browser.new_context()
    yield context
    await context.close()


@pytest.fixture
async def page(context: BrowserContext) -> Page:
    """
    Fixture to provide a new page for each test.
    
    Args:
        context: BrowserContext instance from context fixture
        
    Yields:
        Playwright Page object
    """
    page = await context.new_page()
    yield page
    await page.close()


@pytest.fixture
def base_url() -> str:
    """
    Fixture to provide the base URL for tests.
    
    Returns:
        Base URL from environment or default
    """
    return os.getenv("BASE_URL", "http://localhost:3000")


@pytest.fixture(autouse=False)
async def setup_teardown(page: Page):
    """
    Setup and teardown for each test.
    
    Args:
        page: Page fixture
    """
    # Setup: Navigate to base URL
    base_url = os.getenv("BASE_URL", "http://localhost:3000")
    
    yield
    
    # Teardown: Clear cookies and cache
    await page.context.clear_cookies()


@pytest.fixture
def test_timeout() -> int:
    """
    Fixture to provide test timeout.
    
    Returns:
        Timeout in milliseconds
    """
    return int(os.getenv("TIMEOUT", "30000"))


@pytest.fixture
def headless() -> bool:
    """
    Fixture to determine if browser runs in headless mode.
    
    Returns:
        True for headless, False for headed
    """
    return os.getenv("HEADED", "false").lower() != "true"


def pytest_configure(config):
    """
    Configure pytest with custom markers.
    """
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "critical: mark test as critical test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")


@pytest.fixture
def event_loop():
    """
    Fixture to provide an event loop for async tests.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
