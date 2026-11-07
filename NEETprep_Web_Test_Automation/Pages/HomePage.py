"""
HomePage - Page Object for the logged-in NEETprep dashboard (https://www.neetprep.com/home).

Reached from:
    LoginPage.login_with_otp() returns this object after a successful login.

Provides:
    is_dashboard_visible() -> used by tests to confirm the login worked
    gotoLogout()           -> logs the user out
    gotoDailyDpp()         -> opens Daily DPP (used only by the skipped end-to-end test)
"""
from Pages.BasePage import BasePage
from Pages.dailyDppPage import dailyDppScreen


class HomePage(BasePage):
    def __init__(self, page):
        # Pass the Playwright page up to BasePage (stored as self.page)
        super().__init__(page)

    def gotoDailyDpp(self):
        # NOTE: 'dailyDpp_XPATH' is not defined in conf.ini yet (conf.ini has 'Daily_DPP_XPATH').
        # Add/adjust the locator before un-skipping test_neetprep_end2end.py.
        self.click("dailyDpp_XPATH")
        # Next page in the flow: the Daily DPP screen
        return dailyDppScreen(self.page)

    def gotoLogout(self):
        # Desktop header shows Logout directly; there is no drawer menu or confirmation dialog (Nov 2026)
        self.click("logoutButton_XPATH")
        # Logged out once the landing-page Login/Register link is back
        self.get_element("landingPage_loginButton_XPATH")

    def is_dashboard_visible(self):
        # Gold standard: Check for a unique element on the dashboard
        try:
            # "Custom Practice Session" only exists on the logged-in dashboard
            self.get_element("customPracticeButton_XPATH")
            return True
        except Exception as e:
            # Not found within the timeout -> user is probably not logged in
            #log.logger.error("Dashboard 'customPracticeButton_XPATH' element not found, user may not be logged in.")
            print("Dashboard 'customPracticeButton_XPATH' element not found, user may not be logged in.")
            return False
