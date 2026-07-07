import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import unquote

logger = logging.getLogger(__name__)

class InitPage:
    PROCEED_BUTTON = (By.ID, "proceedBtn")
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def get_attribute(self, locator, attribute) -> str:
        return self.wait.until(EC.presence_of_element_located(locator)).get_attribute(attribute)

    def get_element_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def select_react_dropdown(self, locator, value, send_keys=False, search_text=None):
        """
        Interact with a react-select dropdown.
        """
        field = self.wait.until(EC.element_to_be_clickable(locator))
        if send_keys:
            field.send_keys(search_text if search_text else value)
        else:
            field.click()
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'option')]"))
        )
        self.driver.find_element(
            By.XPATH, f"//div[contains(@id,'option') and contains(text(),'{value}')]"
        ).click()

    def verify_fields_are_empty(self, **fields):
        for name, locator in fields.items():
            logger.info(f"Checking '{name}' field is empty")
            assert self.get_attribute(locator, "value") == "", (
                f"{name} field is not empty"
            )

    def handle_security_page(self, expected_url_text: str, timeout: int = 10):
        """
        Handles security page redirects and waits for the expected URL.
        """

        logger.info("Checking if security page is displayed")

        WebDriverWait(self.driver, timeout).until(
            lambda d: (
                expected_url_text in unquote(d.current_url)
                or d.find_elements(*self.PROCEED_BUTTON)
            )
        )

        if self.driver.find_elements(*self.PROCEED_BUTTON):
            logger.info("Security page detected. Clicking proceed button")

            self.click(self.PROCEED_BUTTON)

            WebDriverWait(self.driver, timeout).until(
                lambda d: expected_url_text in unquote(d.current_url)
            )

        assert expected_url_text in unquote(self.driver.current_url), (
            f"Expected '{expected_url_text}' in URL, "
            f"but got '{self.driver.current_url}'"
        )

        logger.info(
            f"Navigation completed successfully: {self.driver.current_url}"
        )