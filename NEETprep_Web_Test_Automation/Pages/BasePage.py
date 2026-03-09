import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utilities.LogUtil import Logger
from Utilities import configReader

log = Logger(__name__, logging.INFO)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20, poll_frequency=0.5)

    def get_element(self, locator):
        # IMPORTANT: Normalize to lowercase to match configparser behavior
        # This prevents the KeyError: 'mobile_number_id'
        locator_key = locator.lower()

        try:
            locator_value = configReader.readConfig("locators", locator_key)
        except Exception as e:
            log.logger.error(f"Could not find key '{locator_key}' in config file.")
            raise e

        # Using .upper() on the input string to check the suffix safely
        if locator.upper().endswith("_XPATH"):
            by = By.XPATH
        elif locator.upper().endswith("_ID"):
            by = By.ID
        elif locator.upper().endswith("_CSS"):
            by = By.CSS_SELECTOR
        elif locator.upper().endswith("_NAME"):
            by = By.NAME
        elif locator.upper().endswith("_LINKTEXT"):
            by = By.LINK_TEXT
        else:
            log.logger.error(f"Invalid locator suffix for: {locator}")
            return None

        try:
            # Gold standard: wait for visibility
            element = self.wait.until(EC.visibility_of_element_located((by, locator_value)))
            return element
        except TimeoutException:
            log.logger.error(f"FAIL: Element '{locator}' not visible at: {locator_value}")
            # Take screenshot here if you have a screenshot method
            raise

    def type(self, locator, value):
        log.logger.info(f"Step: Typing '{value}' into -> {locator}")
        element = self.get_element(locator)
        element.clear()
        # Adding a tiny sleep or click here can sometimes help if the field has JS listeners
        element.send_keys(str(value))

    def click(self, locator):
        log.logger.info(f"Step: Clicking on Element -> {locator}")
        # 1. Fetch element using your existing get_element logic
        element = self.get_element(locator)

        # 2. Add an extra wait to ensure it's actually interactable
        try:
            self.wait.until(EC.element_to_be_clickable(element))
            element.click()
        except Exception:
            # 3. Industry standard fallback: If normal click fails, force it with JS
            log.logger.info(f"Normal click failed for {locator}, attempting JS click.")
            self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_bottom(self):
        """Uses JavaScript to scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_into_view(self, locator_key):
        """Scrolls until the specific element is visible."""
        xpath_value = configReader.readConfig("locators", locator_key)
        element = self.driver.find_element(By.XPATH, xpath_value)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def is_element_displayed(self, locator):
        """
        Check if an element is visible on the page.
        Returns True if visible, False otherwise.
        """
        try:
            # Reusing your existing get_element logic which handles XPATH/ID/CSS
            element = self.get_element(locator)
            return element.is_displayed()
        except Exception:
            # If element is not found or not visible, return False instead of crashing
            log.logger.error(f"Element {locator} is not displayed on the page.")
            return False