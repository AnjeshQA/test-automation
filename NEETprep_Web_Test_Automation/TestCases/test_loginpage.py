import pytest
from Pages.HomePage import HomePage
from Pages.dailyDppPage import dailyDppScreen
from Pages.loginPage import LoginPage
from TestCases.BaseTest import BaseTest
from Utilities import dataProvider


class Test_LoginPage(BaseTest):
    class Test_LoginPage(BaseTest):

        @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
        def test_valid_login(self, mobileNumber, otp):
            login = LoginPage(self.driver)
            # CHANGED: gotoLoggedIn -> login_with_otp
            # Note: Ensure .gotoLogout() exists in your HomePage class!
            login.login_with_otp(mobileNumber, otp).gotoLogout()

        @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("InvalidCred"))
        def test_invalid_login(self, mobileNumber, otp):
            login = LoginPage(self.driver)
            # CHANGED: gotoLoggedIn -> login_with_invalid_otp
            login.login_with_invalid_otp(mobileNumber, otp)



    # @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
    # def test_loginPage(self, mobileNumber, otp):
    #     login = loginScreen(self.driver)
    #     login.gotoLoggedIn(mobileNumber, otp).gotoDailyDpp()
