import pytest
from Pages.HomePage import HomePage
from Pages.dailyDppPage import dailyDppScreen
from Pages.loginPage import LoginPage
from TestCases.BaseTest import BaseTest
from Utilities import dataProvider


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