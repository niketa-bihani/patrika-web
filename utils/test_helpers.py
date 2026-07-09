"""
Test Utilities and Helpers Module
Common utilities and helper functions for testing.
"""

import asyncio
import random
import string
from datetime import datetime
from typing import TypeVar, Callable, Awaitable, Any, Optional
from playwright.async_api import Page


T = TypeVar("T")


async def wait_for_network_idle(page: Page, timeout: int = 5000) -> None:
    """
    Wait for network to be idle.
    
    Args:
        page: Playwright Page object
        timeout: Timeout in milliseconds
    """
    await page.wait_for_load_state("networkidle", timeout=timeout)


async def wait_for_dom_content_loaded(page: Page, timeout: int = 5000) -> None:
    """
    Wait for DOM content to be loaded.
    
    Args:
        page: Playwright Page object
        timeout: Timeout in milliseconds
    """
    await page.wait_for_load_state("domcontentloaded", timeout=timeout)


async def retry_with_backoff(
    fn: Callable[..., Awaitable[T]],
    max_retries: int = 3,
    delay_ms: int = 1000,
    *args,
    **kwargs
) -> T:
    """
    Retry a function with exponential backoff.
    
    Args:
        fn: Async function to retry
        max_retries: Maximum number of retries
        delay_ms: Initial delay in milliseconds
        *args: Arguments to pass to function
        **kwargs: Keyword arguments to pass to function
        
    Returns:
        Result from the function call
        
    Raises:
        Exception: If all retries fail
    """
    for attempt in range(max_retries):
        try:
            return await fn(*args, **kwargs)
        except Exception as error:
            if attempt == max_retries - 1:
                raise error
            wait_time = delay_ms * (2 ** attempt)
            await asyncio.sleep(wait_time / 1000)
    raise Exception("Retry failed")


def get_random_string(length: int = 10) -> str:
    """
    Generate a random string.
    
    Args:
        length: Length of the string
        
    Returns:
        Random string
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO formatted timestamp
    """
    return datetime.now().isoformat()


def log_step(step_number: int, step_name: str) -> None:
    """
    Log a test step.
    
    Args:
        step_number: Step number
        step_name: Step name/description
    """
    print(f"\n📍 Step {step_number}: {step_name}")


def generate_test_summary(passed: int, failed: int, skipped: int) -> None:
    """
    Generate and print test execution summary.
    
    Args:
        passed: Number of passed tests
        failed: Number of failed tests
        skipped: Number of skipped tests
    """
    summary = f"""
  ╔══════════════════════════════════╗
  ║     TEST EXECUTION SUMMARY       ║
  ╠══════════════════════════════════╣
  ║ ✅ Passed:  {str(passed).ljust(24)} ║
  ║ ❌ Failed:  {str(failed).ljust(24)} ║
  ║ ⏭️  Skipped: {str(skipped).ljust(24)} ║
  ╚══════════════════════════════════╝
  """
    print(summary)


async def wait_and_click(page: Page, selector: str, timeout: int = 5000) -> None:
    """
    Wait for an element and click it.
    
    Args:
        page: Playwright Page object
        selector: CSS selector for the element
        timeout: Timeout in milliseconds
    """
    await page.wait_for_selector(selector, timeout=timeout)
    await page.click(selector)


async def wait_and_fill(page: Page, selector: str, text: str, timeout: int = 5000) -> None:
    """
    Wait for an input element and fill it with text.
    
    Args:
        page: Playwright Page object
        selector: CSS selector for the input element
        text: Text to fill in
        timeout: Timeout in milliseconds
    """
    await page.wait_for_selector(selector, timeout=timeout)
    await page.fill(selector, text)


def get_random_email(domain: str = "example.com") -> str:
    """
    Generate a random email address.
    
    Args:
        domain: Email domain
        
    Returns:
        Random email address
    """
    username = get_random_string(10)
    return f"{username}@{domain}"


async def take_screenshot_on_failure(page: Page, test_name: str) -> None:
    """
    Take a screenshot for failed tests.
    
    Args:
        page: Playwright Page object
        test_name: Name of the test
    """
    import os
    screenshot_dir = "reports/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
    await page.screenshot(path=filename)
    print(f"Screenshot saved: {filename}")
