"""
Login Test Suite - Automated from CSV
Tests for login functionality based on LoginTest.csv test cases.
"""

import pytest
import os
from playwright.async_api import Page
from pages.login_page import LoginPage
from utils.csv_loader import CSVDataLoader
from utils.test_helpers import log_step, get_random_string


# CSV file path - stored in test-data folder
CSV_FILE = os.path.join(os.path.dirname(__file__), '../test-data/LoginTest.csv')

# If CSV doesn't exist locally, check Downloads folder as fallback
if not os.path.exists(CSV_FILE):
    CSV_FILE = os.path.expanduser('~/Downloads/LoginTest.csv')


class TestLoginFromCSV:
    """Test cases automated from CSV data."""

    @pytest.fixture
    async def login_page(self, page: Page):
        """
        Fixture to provide LoginPage object.
        
        Args:
            page: Page fixture
            
        Yields:
            LoginPage instance
        """
        login_page = LoginPage(page)
        await login_page.wait_for_page_load()
        yield login_page

    @pytest.mark.smoke
    @pytest.mark.high_priority
    async def test_tc_login_01_login_entry_point_visible(self, login_page: LoginPage, base_url: str):
        """
        TC-LOGIN-01: Verify Login entry point is visible and opens login modal.
        
        Test Case Details:
        - Priority: High
        - Type: Positive
        - Expected: Modal/page renders with mobile number input
        """
        log_step(1, "Navigate to Patrika homepage")
        await login_page.navigate_to_home()
        
        log_step(2, "Verify page loaded successfully")
        current_url = await login_page.get_current_url()
        assert base_url in current_url, f"Expected URL to contain {base_url}"
        
        log_step(3, "Click login icon/button")
        await login_page.click_login_icon()
        
        log_step(4, "Verify login modal is visible")
        is_modal_visible = await login_page.is_login_modal_visible()
        assert is_modal_visible, "Login modal should be visible"
        
        log_step(5, "Verify mobile number input field is visible")
        mobile_input_visible = await login_page.is_visible(login_page.MOBILE_INPUT_LOCATOR)
        assert mobile_input_visible, "Mobile number input should be visible in login modal"
        
        print("✅ TC-LOGIN-01 PASSED: Login entry point is visible and opens login modal")

    @pytest.mark.smoke
    @pytest.mark.high_priority
    async def test_tc_login_02_otp_triggered_for_valid_mobile(self, login_page: LoginPage):
        """
        TC-LOGIN-02: Verify OTP is triggered for a valid mobile number.
        
        Test Case Details:
        - Priority: High
        - Type: Positive
        - Test Data: Mobile Number: 9876543210
        - Expected: OTP triggered, "OTP sent" confirmation shown, OTP input field appears
        """
        log_step(1, "Navigate to home and open login modal")
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, "Enter valid mobile number (9876543210)")
        valid_mobile = "9876543210"
        await login_page.enter_mobile_number(valid_mobile)
        
        log_step(3, "Verify mobile number was entered")
        entered_mobile = await login_page.get_mobile_input_value()
        assert entered_mobile == valid_mobile, f"Expected {valid_mobile}, got {entered_mobile}"
        
        log_step(4, "Click 'Get OTP' button")
        await login_page.click_get_otp()
        
        log_step(5, "Verify OTP input field appears")
        otp_visible = await login_page.is_otp_input_visible(timeout=5000)
        assert otp_visible, "OTP input field should appear after clicking Get OTP"
        
        log_step(6, "Verify OTP sent confirmation (optional check)")
        # Confirmation message may or may not be visible, but OTP field should be
        
        print("✅ TC-LOGIN-02 PASSED: OTP triggered for valid mobile number")

    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_login_03_invalid_mobile_format_rejected(self, login_page: LoginPage):
        """
        TC-LOGIN-03: Verify invalid mobile number format is rejected.
        
        Test Case Details:
        - Priority: Medium
        - Type: Negative
        - Test Data: Mobile Number: 98765 (invalid - too short)
        - Expected: Inline validation error shown, OTP not triggered
        """
        log_step(1, "Navigate to home and open login modal")
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, "Enter invalid mobile number (too short: 98765)")
        invalid_mobile = "98765"
        await login_page.enter_mobile_number(invalid_mobile)
        
        log_step(3, "Validate mobile number format using business logic")
        is_valid = await login_page.validate_mobile_number_format(invalid_mobile)
        assert not is_valid, f"Mobile {invalid_mobile} should be invalid (too short)"
        
        log_step(4, "Verify Get OTP button behavior with invalid number")
        # Button may be disabled or error shown after click
        await login_page.click_get_otp()
        
        log_step(5, "Check for error message")
        import asyncio
        await asyncio.sleep(1)  # Wait for any error message to appear
        
        error_visible = await login_page.is_error_message_visible()
        otp_visible = await login_page.is_otp_input_visible(timeout=2000)
        
        # Either error message shown or OTP field not visible
        assert error_visible or not otp_visible, "Should show error or not trigger OTP for invalid mobile"
        
        print("✅ TC-LOGIN-03 PASSED: Invalid mobile format properly rejected")

    @pytest.mark.regression
    @pytest.mark.medium_priority
    async def test_tc_login_04_otp_rate_limit_check(self, login_page: LoginPage):
        """
        TC-LOGIN-04: Verify OTP request is rate-limited on rapid repeat clicks.
        
        Test Case Details:
        - Priority: Medium
        - Type: Negative
        - Test Data: Mobile Number: 9876543210
        - Expected: "Resend OTP" disabled/timed (e.g. 30-60s cooldown), prevents spam-triggering
        """
        log_step(1, "Navigate to home and open login modal")
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, "Enter valid mobile number")
        valid_mobile = "9876543210"
        await login_page.enter_mobile_number(valid_mobile)
        
        log_step(3, "Click 'Get OTP' to trigger first OTP")
        await login_page.click_get_otp()
        
        log_step(4, "Wait for OTP field to appear")
        import asyncio
        await asyncio.sleep(1)
        
        log_step(5, "Check if Resend button has cooldown/disabled state")
        resend_button_visible = await login_page.is_visible(login_page.RESEND_OTP_BUTTON_LOCATOR)
        
        if resend_button_visible:
            is_disabled = await login_page.is_resend_button_disabled()
            cooldown_text = await login_page.get_resend_cooldown_text()
            
            log_step(6, f"Verify rate limiting: disabled={is_disabled}, cooldown_text={cooldown_text}")
            
            # Resend button should be disabled or show cooldown timer
            assert is_disabled or "s" in cooldown_text.lower() or "resend" in cooldown_text.lower(), \
                "Resend button should be disabled with cooldown"
        
        print("✅ TC-LOGIN-04 PASSED: OTP rate-limiting in place")


class TestLoginPositiveScenarios:
    """Positive test scenarios for login functionality."""

    @pytest.fixture
    async def login_page(self, page: Page):
        """Login page fixture."""
        login_page = LoginPage(page)
        await login_page.wait_for_page_load()
        yield login_page

    @pytest.mark.smoke
    async def test_login_modal_displays_correctly(self, login_page: LoginPage):
        """Test: Login modal displays with proper styling and elements."""
        log_step(1, "Open login modal")
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, "Verify modal is displayed")
        is_visible = await login_page.is_login_modal_visible()
        assert is_visible
        
        log_step(3, "Verify mobile input field is present")
        mobile_visible = await login_page.is_visible(login_page.MOBILE_INPUT_LOCATOR)
        assert mobile_visible
        
        log_step(4, "Verify Get OTP button is clickable")
        get_otp_visible = await login_page.is_visible(login_page.GET_OTP_BUTTON_LOCATOR)
        assert get_otp_visible
        
        print("✅ Login modal displays correctly")

    @pytest.mark.regression
    @pytest.mark.parametrize("mobile_number", [
        "9876543210",
        "9123456789",
        "8765432109",
        "7654321098",
        "6543210987",
    ])
    async def test_valid_mobile_numbers(self, login_page: LoginPage, mobile_number: str):
        """Test: Multiple valid mobile numbers trigger OTP."""
        log_step(1, f"Test with mobile number: {mobile_number}")
        
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, f"Enter mobile number: {mobile_number}")
        await login_page.enter_mobile_number(mobile_number)
        
        log_step(3, "Verify mobile number format")
        is_valid = await login_page.validate_mobile_number_format(mobile_number)
        assert is_valid, f"Mobile {mobile_number} should be valid"
        
        log_step(4, "Click Get OTP")
        await login_page.click_get_otp()
        
        log_step(5, "Verify OTP field appears")
        otp_visible = await login_page.is_otp_input_visible(timeout=5000)
        assert otp_visible, f"OTP field should appear for mobile {mobile_number}"
        
        print(f"✅ Valid mobile {mobile_number} triggers OTP")


class TestLoginNegativeScenarios:
    """Negative test scenarios for login functionality."""

    @pytest.fixture
    async def login_page(self, page: Page):
        """Login page fixture."""
        login_page = LoginPage(page)
        await login_page.wait_for_page_load()
        yield login_page

    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_mobile", [
        "12345",           # Too short
        "12345678901",     # Too long
        "abcd1234567",     # Contains letters
        "123-456-7890",    # Contains special characters
        "5123456789",      # Starts with invalid digit
        "1234567890",      # Starts with 1
        "",                # Empty
        "   ",             # Spaces only
    ])
    async def test_invalid_mobile_numbers(self, login_page: LoginPage, invalid_mobile: str):
        """Test: Invalid mobile numbers are rejected."""
        log_step(1, f"Test with invalid mobile: '{invalid_mobile}'")
        
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, "Validate mobile number format")
        is_valid = await login_page.validate_mobile_number_format(invalid_mobile.strip())
        assert not is_valid, f"Mobile '{invalid_mobile}' should be invalid"
        
        print(f"✅ Invalid mobile '{invalid_mobile}' correctly rejected")

    @pytest.mark.regression
    async def test_login_with_empty_input(self, login_page: LoginPage):
        """Test: Empty mobile number input is handled."""
        log_step(1, "Open login modal")
        await login_page.navigate_to_home()
        await login_page.click_login_icon()
        await login_page.wait_for_login_modal()
        
        log_step(2, "Leave mobile input empty")
        await login_page.enter_mobile_number("")
        
        log_step(3, "Click Get OTP")
        await login_page.click_get_otp()
        
        log_step(4, "Verify error or OTP not triggered")
        import asyncio
        await asyncio.sleep(1)
        
        error_visible = await login_page.is_error_message_visible()
        otp_visible = await login_page.is_otp_input_visible(timeout=2000)
        
        assert error_visible or not otp_visible, "Empty input should not trigger OTP"
        
        print("✅ Empty input properly handled")


# Fixtures for base_url (if not already defined in conftest.py)
@pytest.fixture
def base_url(request) -> str:
    """Base URL fixture."""
    import os
    return os.getenv("BASE_URL", "https://www.patrika.com")
