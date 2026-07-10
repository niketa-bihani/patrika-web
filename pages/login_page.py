"""
Login Page Object
Contains selectors and methods for login page interactions.
"""

from playwright.async_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object containing selectors and page-specific methods."""

    # Selectors matched against the LIVE patrika.com DOM (verified 2026-07).
    # NOTE: Login is a SEPARATE PAGE at /login, NOT a modal. The site is in Hindi,
    # so button labels are Hindi text. The mobile field enables "Get OTP" only
    # after a valid 10-digit number is entered. OTP is 6 single-char boxes.
    LOGIN_ICON_LOCATOR = "a[href='/login']"
    # There is no dialog; the login "form" is considered present when the mobile
    # input is on screen. Kept the name LOGIN_MODAL_LOCATOR for test compatibility.
    LOGIN_MODAL_LOCATOR = "input[type='tel'][placeholder='0000000000']"
    MOBILE_INPUT_LOCATOR = "input[type='tel'][placeholder='0000000000']"
    GET_OTP_BUTTON_LOCATOR = "button:has-text('OTP प्राप्त करें')"          # "Get OTP"
    OTP_INPUT_LOCATOR = "input[type='tel'][maxlength='1']"                   # 6 segmented boxes
    VERIFY_OTP_BUTTON_LOCATOR = "button:has-text('सत्यापित करें')"          # "Verify"
    CHANGE_NUMBER_BUTTON_LOCATOR = "button:has-text('नंबर बदलें')"          # "Change number"
    RESEND_OTP_BUTTON_LOCATOR = "button:has-text('OTP')"                    # resend/get-otp area
    ERROR_MESSAGE_LOCATOR = ".MuiFormHelperText-root.Mui-error, .Mui-error, [role='alert']"
    OTP_SENT_CONFIRMATION_LOCATOR = "input[type='tel'][maxlength='1']"      # OTP boxes appear
    RESEND_COOLDOWN_LOCATOR = "button:has-text('OTP')"

    def __init__(self, page: Page):
        """
        Initialize the Login Page object.
        
        Args:
            page: Playwright Page object
        """
        super().__init__(page)

    async def navigate_to_home(self) -> None:
        """Navigate to home page before login."""
        await self.goto("/")

    async def click_login_icon(self) -> None:
        """Click the login link; this NAVIGATES to the /login page (no modal)."""
        try:
            await self.click(self.LOGIN_ICON_LOCATOR)
            # Login is a full page navigation, not a modal — wait for the form.
            await self.page.wait_for_url("**/login", timeout=10000)
        except Exception as e:
            print(f"Login icon click failed: {e}")
            raise

    async def is_login_modal_visible(self) -> bool:
        """
        Check if login modal is visible.
        
        Returns:
            True if login modal is visible, False otherwise
        """
        try:
            return await self.is_visible(self.LOGIN_MODAL_LOCATOR)
        except:
            return False

    async def wait_for_login_modal(self, timeout: int = 5000) -> None:
        """
        Wait for login modal to appear.
        
        Args:
            timeout: Timeout in milliseconds
        """
        await self.wait_for_element(self.LOGIN_MODAL_LOCATOR, timeout)

    async def enter_mobile_number(self, mobile_number: str) -> None:
        """
        Enter mobile number in the input field.
        
        Args:
            mobile_number: 10-digit mobile number
        """
        await self.fill_input(self.MOBILE_INPUT_LOCATOR, mobile_number)

    async def click_get_otp(self) -> None:
        """
        Click 'Get OTP' (OTP प्राप्त करें).

        The site keeps this button DISABLED until a valid 10-digit mobile number
        is entered. Clicking a disabled button would make Playwright auto-wait
        until timeout, so we skip the click when it is disabled — the disabled
        state itself is the site's rejection of an invalid number.
        """
        btn = self.page.locator(self.GET_OTP_BUTTON_LOCATOR).first
        try:
            if await btn.is_disabled():
                return
        except Exception:
            pass
        await btn.click()

    async def is_otp_sent_confirmation_visible(self, timeout: int = 5000) -> bool:
        """
        Check if OTP sent confirmation message is visible.
        
        Args:
            timeout: Timeout in milliseconds
            
        Returns:
            True if confirmation is visible, False otherwise
        """
        try:
            await self.wait_for_element(self.OTP_SENT_CONFIRMATION_LOCATOR, timeout)
            return True
        except:
            return False

    async def is_otp_input_visible(self, timeout: int = 5000) -> bool:
        """
        Check if OTP input field is visible.
        
        Args:
            timeout: Timeout in milliseconds
            
        Returns:
            True if OTP input is visible, False otherwise
        """
        try:
            await self.wait_for_element(self.OTP_INPUT_LOCATOR, timeout)
            return True
        except:
            return False

    async def get_error_message(self) -> str:
        """
        Get error message text if displayed.
        
        Returns:
            Error message text
        """
        try:
            return await self.get_text(self.ERROR_MESSAGE_LOCATOR)
        except:
            return ""

    async def is_error_message_visible(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error message is visible, False otherwise
        """
        return await self.is_visible(self.ERROR_MESSAGE_LOCATOR)

    async def enter_otp(self, otp: str) -> None:
        """
        Enter OTP in the OTP input field.
        
        Args:
            otp: OTP code
        """
        await self.fill_input(self.OTP_INPUT_LOCATOR, otp)

    async def click_verify_otp(self) -> None:
        """Click 'Verify' button to submit OTP."""
        await self.click(self.VERIFY_OTP_BUTTON_LOCATOR)

    async def click_resend_otp(self) -> None:
        """Click 'Resend OTP' button."""
        await self.click(self.RESEND_OTP_BUTTON_LOCATOR)

    async def is_resend_button_disabled(self) -> bool:
        """
        Check if 'Resend OTP' button is disabled (rate-limited).
        
        Returns:
            True if button is disabled, False otherwise
        """
        try:
            is_disabled = await self.page.is_disabled(self.RESEND_OTP_BUTTON_LOCATOR)
            return is_disabled
        except:
            return False

    async def get_resend_cooldown_text(self) -> str:
        """
        Get the cooldown timer text from resend button.
        
        Returns:
            Cooldown timer text (e.g., "30s")
        """
        try:
            return await self.get_text(self.RESEND_COOLDOWN_LOCATOR)
        except:
            return ""

    async def login_with_mobile(self, mobile_number: str) -> None:
        """
        Complete login flow with mobile number.
        
        Args:
            mobile_number: 10-digit mobile number
        """
        await self.navigate_to_home()
        await self.click_login_icon()
        await self.wait_for_login_modal()
        await self.enter_mobile_number(mobile_number)
        await self.click_get_otp()

    async def validate_mobile_number_format(self, mobile_number: str) -> bool:
        """
        Validate mobile number format (10 digits, starts with 6-9).
        
        Args:
            mobile_number: Mobile number to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if not mobile_number or len(mobile_number) != 10:
            return False
        if not mobile_number.isdigit():
            return False
        if not mobile_number[0] in ['6', '7', '8', '9']:
            return False
        return True

    async def get_mobile_input_value(self) -> str:
        """
        Get the current value of mobile input field.
        
        Returns:
            Mobile number entered in input field
        """
        try:
            return await self.page.input_value(self.MOBILE_INPUT_LOCATOR)
        except:
            return ""

    async def clear_mobile_input(self) -> None:
        """Clear the mobile number input field."""
        await self.page.fill(self.MOBILE_INPUT_LOCATOR, "")

    async def wait_for_resend_button_enabled(self, timeout: int = 90000) -> None:
        """
        Wait for 'Resend OTP' button to become enabled (cooldown expires).
        
        Args:
            timeout: Timeout in milliseconds (default 90 seconds)
        """
        async def is_enabled():
            is_disabled = await self.is_resend_button_disabled()
            return not is_disabled
        
        from utils.test_helpers import retry_with_backoff
        await retry_with_backoff(self.is_visible, self.RESEND_OTP_BUTTON_LOCATOR)

    async def close_login_modal(self) -> None:
        """Close login modal (if there's a close button)."""
        close_button_locators = [
            "button[aria-label='Close'], button:has-text('×'), button.close-btn"
        ]
        
        for locator in close_button_locators:
            try:
                if await self.is_visible(locator):
                    await self.click(locator)
                    return
            except:
                continue
        
        raise Exception("Close button not found on login modal")

    async def wait_for_page_load(self) -> None:
        """Wait for page to fully load before testing."""
        await self.wait_for_load_state("networkidle", timeout=10000)
