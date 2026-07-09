"""
Base Page class for all page objects in the automation framework.
Provides common utilities for page interactions.
"""

from playwright.async_api import Page
import os


class BasePage:
    """
    Base class for all page objects.
    Contains common methods for page interactions and navigation.
    """

    def __init__(self, page: Page):
        """
        Initialize the base page with a Playwright page object.
        
        Args:
            page: Playwright Page object
        """
        self.page = page

    async def goto(self, url: str) -> None:
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
        """
        await self.page.goto(url)

    async def fill_input(self, selector: str, text: str) -> None:
        """
        Fill an input field with text.
        
        Args:
            selector: CSS selector for the input element
            text: Text to fill in
        """
        await self.page.fill(selector, text)

    async def click(self, selector: str) -> None:
        """
        Click on an element.
        
        Args:
            selector: CSS selector for the element
        """
        await self.page.click(selector)

    async def get_text(self, selector: str) -> str:
        """
        Get text content of an element.
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            Text content of the element
        """
        return await self.page.text_content(selector)

    async def is_visible(self, selector: str) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            True if visible, False otherwise
        """
        return await self.page.is_visible(selector)

    async def wait_for_element(self, selector: str, timeout: int = 5000) -> None:
        """
        Wait for an element to appear.
        
        Args:
            selector: CSS selector for the element
            timeout: Maximum time to wait in milliseconds
        """
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def take_screenshot(self, filename: str) -> None:
        """
        Take a screenshot and save it.
        
        Args:
            filename: Name of the screenshot file
        """
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        await self.page.screenshot(path=f"{screenshot_dir}/{filename}")

    async def get_page_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            Page title
        """
        return await self.page.title()

    async def get_current_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            Current URL
        """
        return self.page.url

    async def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000) -> None:
        """
        Wait for a specific page load state.
        
        Args:
            state: Load state to wait for (networkidle, domcontentloaded, load)
            timeout: Maximum time to wait in milliseconds
        """
        await self.page.wait_for_load_state(state, timeout=timeout)

    async def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Get an attribute value from an element.
        
        Args:
            selector: CSS selector for the element
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        return await self.page.get_attribute(selector, attribute)

    async def press_key(self, key: str) -> None:
        """
        Press a keyboard key.
        
        Args:
            key: Key to press (e.g., 'Enter', 'Escape', 'Tab')
        """
        await self.page.press(key)

    async def reload(self) -> None:
        """Reload the current page."""
        await self.page.reload()

    async def go_back(self) -> None:
        """Navigate back to the previous page."""
        await self.page.go_back()

    async def go_forward(self) -> None:
        """Navigate forward to the next page."""
        await self.page.go_forward()
