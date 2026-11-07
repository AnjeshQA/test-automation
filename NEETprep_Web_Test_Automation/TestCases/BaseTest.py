"""
BaseTest - parent class for class-based (non-BDD) tests, e.g. test_loginpage.py.

Purpose:
    Inherit from it and every test method automatically gets:
      - self.page         (via the "setup" fixture in conftest.py)
      - failure screenshot in Allure (via the "log_on_failure" fixture)
      - one automatic re-run if the test fails (flaky marker, pytest-rerunfailures)

Usage:
    class Test_Something(BaseTest):
        def test_x(self):
            LoginPage(self.page).login_with_otp(...)
"""
import logging
import pytest

# Setting up logging so you can see what's happening in the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Re-run a failed test once before reporting it as failed
@pytest.mark.flaky(reruns=1)
# IMPORTANT: "setup" must match the function name in conftest.py
# "log_on_failure" handles the automatic screenshots
@pytest.mark.usefixtures("setup", "log_on_failure")
class BaseTest:
    pass
