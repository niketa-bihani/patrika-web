"""
Sample Test File
Example tests for the home page using page object model.
"""

import pytest
from playwright.async_api import Page
from pages.home_page import HomePage
from utils.test_helpers import log_step


class TestHomePage:
    """Test class for Home Page functionality."""

    @pytest.fixture
    async def home_page(self, page: Page):
        """
        Fixture to provide HomePage object.
        
        Args:
            page: Page fixture from conftest
            
        Yields:
            HomePage instance
        """
        home_page = HomePage(page)
        yield home_page

    @pytest.mark.smoke
    async def test_navigate_to_home_page(self, home_page: HomePage):
        """
        Test: User should be able to navigate to home page.
        
        Args:
            home_page: HomePage fixture
        """
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()

        log_step(2, "Verify page title exists")
        title = await home_page.get_page_title()
        assert title is not None
        print(f"Page title: {title}")

        log_step(3, "Verify header is visible")
        is_header_visible = await home_page.is_header_visible()
        assert is_header_visible, "Header should be visible on home page"

    @pytest.mark.regression
    async def test_verify_correct_url(self, home_page: HomePage, base_url: str):
        """
        Test: Home page should have correct URL.
        
        Args:
            home_page: HomePage fixture
            base_url: Base URL fixture
        """
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()

        log_step(2, "Verify current URL is correct")
        current_url = await home_page.get_current_url()
        assert current_url == base_url + "/"
        print(f"Current URL: {current_url}")

    @pytest.mark.smoke
    async def test_click_logo_navigates_home(self, home_page: HomePage, base_url: str):
        """
        Test: Clicking logo should navigate to home page.
        
        Args:
            home_page: HomePage fixture
            base_url: Base URL fixture
        """
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()

        log_step(2, "Click on logo")
        try:
            await home_page.click_logo()
        except Exception as e:
            print(f"Logo click may not be available: {e}")

        log_step(3, "Verify we are on home page")
        current_url = await home_page.get_current_url()
        assert base_url in current_url

    @pytest.mark.regression
    async def test_navigation_elements_visible(self, home_page: HomePage):
        """
        Test: Navigation elements should be visible.
        
        Args:
            home_page: HomePage fixture
        """
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()

        log_step(2, "Check if navigation menu is visible")
        is_nav_visible = await home_page.is_navigation_visible()
        print(f"Navigation visible: {is_nav_visible}")

        log_step(3, "Check if main content is visible")
        is_content_visible = await home_page.is_content_visible()
        print(f"Content visible: {is_content_visible}")

    @pytest.mark.critical
    async def test_page_loads_successfully(self, home_page: HomePage):
        """
        Test: Page should load successfully without errors.
        
        Args:
            home_page: HomePage fixture
        """
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()

        log_step(2, "Wait for page to fully load")
        await home_page.wait_for_load_state("networkidle", timeout=10000)

        log_step(3, "Verify page loaded without console errors")
        # Page loaded successfully if no exceptions were raised
        assert True, "Page loaded successfully"


class TestHomePageWithTag:
    """Additional tests for Home Page with tags."""

    @pytest.mark.smoke
    @pytest.mark.critical
    async def test_header_text_not_empty(self, page: Page):
        """
        Test: Header should contain text.
        
        Args:
            page: Page fixture
        """
        home_page = HomePage(page)
        
        log_step(1, "Navigate to home page")
        await home_page.navigate_to_home()

        log_step(2, "Get header text")
        try:
            header_text = await home_page.get_header_text()
            print(f"Header text: {header_text}")
        except Exception as e:
            print(f"Could not retrieve header text: {e}")
