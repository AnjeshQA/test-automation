from Pages.BasePage import BasePage
from Pages.dailyDppPage import dailyDppScreen


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def gotoDailyDpp(self):
        self.click("dailyDpp_XPATH")
        return dailyDppScreen(self.page)

    def gotoLogout(self):
        # Desktop header shows Logout directly; there is no drawer menu or confirmation dialog (Nov 2026)
        self.click("logoutButton_XPATH")
        # Logged out once the landing-page Login/Register link is back
        self.get_element("landingPage_loginButton_XPATH")

    def is_dashboard_visible(self):
        # Gold standard: Check for a unique element on the dashboard
        try:
            self.get_element("customPracticeButton_XPATH")
            return True
        except Exception as e:
            #log.logger.error("Dashboard 'customPracticeButton_XPATH' element not found, user may not be logged in.")
            print("Dashboard 'customPracticeButton_XPATH' element not found, user may not be logged in.")
            return False