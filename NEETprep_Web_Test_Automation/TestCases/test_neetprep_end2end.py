"""
End-to-end flow: login -> Daily DPP -> answer a question.

STATUS: SKIPPED (see @pytest.mark.skip below).
    This was originally a mobile (Appium) test. The Daily DPP locators used by
    HomePage.gotoDailyDpp() and dailyDppScreen.dailyDpp() are not in conf.ini yet.

To enable it later:
    1. Add the Daily DPP locators to ConfigurationData/conf.ini.
    2. Note: each test gets a fresh browser, so test_02/test_03 must first log in
       (or merge the three steps into one test).
    3. Remove the @pytest.mark.skip line.
"""
import pytest
from Pages.HomePage import HomePage
from Pages.dailyDppPage import dailyDppScreen
from Pages.loginPage import LoginPage
from TestCases.BaseTest import BaseTest
from Utilities import dataProvider


# Every test below runs once per "UserDetail" Excel row
@pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
@pytest.mark.skip(reason="Not running this for now to avoid failures")
class Test_NeetPrep_EndToEnd(BaseTest):

    def test_01_login_step(self, mobileNumber, otp):
        """Step 1: Handle the login process."""
        self.login = LoginPage(self.page)
        print(f"Starting Login with: {mobileNumber}")

        # This performs the phone entry and OTP verification
        self.login.login_with_otp(mobileNumber, otp)

    def test_02_navigate_to_dpp(self, mobileNumber, otp):
        """Step 2: Start from Home and navigate to Daily DPP."""
        # The app is already logged in from the previous step
        self.home = HomePage(self.page)
        print("Navigating to Daily DPP...")

        self.home.gotoDailyDpp()

    def test_03_perform_dpp_actions(self, mobileNumber, otp):
        """Step 3: Perform actions on the Daily DPP screen."""
        # The app is already on the Daily DPP screen
        self.dpp = dailyDppScreen(self.page)
        print("Executing Daily DPP test logic...")

        self.dpp.dailyDpp()
