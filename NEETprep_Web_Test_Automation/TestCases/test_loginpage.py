import pytest
from Pages.HomePage import HomePage
from Pages.dailyDppPage import dailyDppScreen
from Pages.loginPage import LoginPage
from TestCases.BaseTest import BaseTest
from Utilities import configReader, dataProvider


class Test_LoginPage(BaseTest):

    @pytest.fixture(autouse=True)
    def open_site(self, setup):
        # The Selenium version never opened the site before logging in
        self.page.goto(configReader.readConfig("common info", "url"), wait_until="domcontentloaded")

    @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
    def test_valid_login(self, mobileNumber, otp):
        login = LoginPage(self.page)
        # CHANGED: gotoLoggedIn -> login_with_otp
        # Note: Ensure .gotoLogout() exists in your HomePage class!
        login.login_with_otp(mobileNumber, otp).gotoLogout()

    @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("InvalidCred"))
    def test_invalid_login(self, mobileNumber, otp):
        login = LoginPage(self.page)
        # CHANGED: gotoLoggedIn -> login_with_invalid_otp
        login.login_with_invalid_otp(mobileNumber, otp)



    # @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))
    # def test_loginPage(self, mobileNumber, otp):
    #     login = loginScreen(self.page)
    #     login.gotoLoggedIn(mobileNumber, otp).gotoDailyDpp()
