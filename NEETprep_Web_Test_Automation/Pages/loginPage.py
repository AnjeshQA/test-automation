"""
LoginPage - Page Object for the NEETprep landing page + OTP login form (https://www.neetprep.com).

Used by:
    TestCases/test_login_bdd.py   (BDD scenario "Successful login via OTP")
    TestCases/test_loginpage.py   (valid / invalid login tests)

Flow:
    landing page -> close popup -> Login/Register -> mobile number -> accept T&C
    -> Send OTP -> enter OTP -> Verify -> HomePage (dashboard)

Next step after login:
    login_with_otp() returns a HomePage object, so tests can chain e.g.
    LoginPage(page).login_with_otp(mobile, otp).gotoLogout()
"""
from Pages.BasePage import BasePage
from Pages.HomePage import HomePage


class LoginPage(BasePage):
    """
    Industry-standard Page Object.
    Logic is decoupled from locators to ensure easy maintenance.
    """

    def __init__(self, page):
        # Pass the Playwright page up to BasePage (stored as self.page)
        super().__init__(page)

    def login_with_otp(self, mobile_number, otp):
        """Standard login flow for valid credentials."""
        # Using keys that match your ConfigurationData/conf.ini
        # 1. Close the promotional "classroom" popup shown on the landing page
        self.click("landingPage_close_classroom_dialogBox_XPATH")
        # 2. Open the login page from the header's Login/Register link
        self.click("landingPage_loginButton_XPATH")
        # 3. Enter the mobile number (from Excel test data)
        self.type("login_enterMobileNo_XPATH", mobile_number)
        # 4. Tick the Terms of Use consent checkbox (Send OTP stays disabled until ticked)
        self.click("login_TC_constant_checkBox_XPATH")
        # 5. Request the OTP
        self.click("login_sendOTP_button_XPATH")
        # 6. Enter the OTP (from Excel test data; the test account uses a fixed OTP)
        self.type("login_enterOTP_XPATH", otp)
        # 7. Make sure the Verify button is in view, then submit
        self.scroll_into_view("login_verifyOTP_XPATH")
        self.click("login_verifyOTP_XPATH")
        # 8. Next page in the flow: the logged-in dashboard
        return HomePage(self.page)

    def login_with_invalid_otp(self, mobile_number, otp):
        """Negative test flow verifying error message visibility."""
        self.login_with_otp(mobile_number, otp)  # Reuse existing logic

        # Verify result via BasePage helper: the "Invalid OTP" message must appear
        is_error = self.is_element_displayed("invalid_OTP_error_message_XPATH")
        assert is_error, "FAILED: 'Invalid OTP' error message was NOT visible!"
        # Stay on the login page object (user is not logged in)
        return self
