import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Utilities import configReader


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'  # Start as soon as DOM is ready

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Force a large window size to ensure the desktop header (and search icon) is visible
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)  # Set to autouse so it always monitors
def log_on_failure(request, driver):
    """
    Captures screenshots on failure and attaches them to the Allure report.
    """
    yield
    item = request.node
    if hasattr(item, "rep_call") and item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(),
                      name="failure_screenshot",
                      attachment_type=allure.attachment_type.PNG)