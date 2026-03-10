from Pages.BasePage import BasePage
from Pages.dailyDppPage import dailyDppScreen


class HomePage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)

    def gotoDailyDpp(self):
        self.click("dailyDpp_XPATH")
        return dailyDppScreen(self.driver)

    def gotoLogout(self):
        self.click("drawerMenu_XPATH")

        self.click("logoutButton_ID")

        self.click("logoutConfirmation_ID")

    def is_dashboard_visible(self):
        # Gold standard: Check for a unique element on the dashboard
        try:
            self.get_element("customPracticeButton_XPATH")
            return True
        except Exception as e:
            #log.logger.error("Dashboard 'customPracticeButton_XPATH' element not found, user may not be logged in.")
            print("Dashboard 'customPracticeButton_XPATH' element not found, user may not be logged in.")
            return False