from Pages.BasePage import BasePage
from Pages.HomePage import HomePage


class LoginPage(BasePage):
    """
    Industry-standard Page Object.
    Logic is decoupled from locators to ensure easy maintenance.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def login_with_otp(self, mobile_number, otp):
        """Standard login flow for valid credentials."""
        # Using keys that match your ConfigurationData/conf.ini
        self.click("landingPage_close_classroom_dialogBox_XPATH")
        self.click("landingPage_loginButton_XPATH")
        self.type("login_enterMobileNo_XPATH", mobile_number)
        self.click("login_TC_constant_checkBox_XPATH")
        self.click("login_sendOTP_button_XPATH")
        self.type("login_enterOTP_XPATH", otp)
        self.scroll_into_view("login_verifyOTP_XPATH")
        self.click("login_verifyOTP_XPATH")
        return HomePage(self.driver)

    def login_with_invalid_otp(self, mobile_number, otp):
        """Negative test flow verifying error message visibility."""
        self.login_with_otp(mobile_number, otp)  # Reuse existing logic

        # Verify result via BasePage helper
        is_error = self.is_element_displayed("invalid_OTP_error_message_XPATH")
        assert is_error, "FAILED: 'Invalid OTP' error message was NOT visible!"
        return self