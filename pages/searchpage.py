import logging
from pages.init_page import InitPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
logger = logging.getLogger(__name__)

class SearchPage(InitPage):
    SEARCH_BOX_ID = "search"
    SEARCH_BUTTON_ID = "varsome-search-btn"
    SEARCH_DROPDOWN_CLASS = "select-selected"
    SEARCH_MODAL = (By.CSS_SELECTOR, "[data-testid='modal']")
    ACMG_CARD = (By.CSS_SELECTOR, "[data-testid='acmg']")
    WARNING_BUTTON = (By.XPATH, "//button[contains(text(),'I understand')]")
    VARIANT_INFO = (By.ID, "variant-info")
    

    def verify_sections_are_displayed(self, *sections, timeout: int = 10):
        for section in sections:
            logger.info(f"Checking section: {section}")

            locator = (
                By.XPATH,
                f"//span[contains(normalize-space(), '{section}')]"
            )

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )

            except TimeoutException:
                raise AssertionError(
                    f"Section '{section}' was not found or not visible "
                    f"after {timeout} seconds"
                )

    def wait_for_results_loading(self, timeout: int = 20):
        """
        Wait until the variant information section is visible.
        """

        logger.info("Waiting for variant information to load")

        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.VARIANT_INFO)
        )

        logger.info("Variant information loaded successfully")