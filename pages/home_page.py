"""
Home Page Object
Contains selectors and methods for home page interactions.
"""

from playwright.async_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object containing selectors and page-specific methods."""

    # Selectors
    HEADER_LOCATOR = "header"
    LOGO_LOCATOR = 'a[href="/"]'
    NAVIGATION_MENU_LOCATOR = "nav"
    CONTENT_LOCATOR = "main"

    def __init__(self, page: Page):
        """
        Initialize the Home Page object.
        
        Args:
            page: Playwright Page object
        """
        super().__init__(page)

    async def navigate_to_home(self) -> None:
        """Navigate to the home page."""
        await self.goto("/")

    async def is_header_visible(self) -> bool:
        """
        Check if the header is visible.
        
        Returns:
            True if header is visible, False otherwise
        """
        return await self.is_visible(self.HEADER_LOCATOR)

    async def click_logo(self) -> None:
        """Click on the logo to navigate to home."""
        await self.click(self.LOGO_LOCATOR)

    async def get_header_text(self) -> str:
        """
        Get header text content.
        
        Returns:
            Header text
        """
        return await self.get_text(self.HEADER_LOCATOR)

    async def is_navigation_visible(self) -> bool:
        """
        Check if navigation menu is visible.
        
        Returns:
            True if navigation is visible, False otherwise
        """
        return await self.is_visible(self.NAVIGATION_MENU_LOCATOR)

    async def is_content_visible(self) -> bool:
        """
        Check if main content area is visible.
        
        Returns:
            True if content is visible, False otherwise
        """
        return await self.is_visible(self.CONTENT_LOCATOR)
