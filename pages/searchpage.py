import logging
from pages.init_page import InitPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
    
logger = logging.getLogger(__name__)

class SearchPage(InitPage):
    SEARCH_BOX_ID = "search"
    SEARCH_BUTTON_ID = "varsome-search-btn"
    SEARCH_DROPDOWN_CLASS = "select-selected"
    SEARCH_MODAL = "[data-testid='modal']"
    ACMG_CARD = "[data-testid='acmg']"
    WARNING_BUTTON = "button[contains(text(),'I understand')]"
    
    def verify_sections_are_displayed(self, *sections):
        for section in sections:
            logger.info(f"Checking section: {section}")

            assert self.driver.find_elements(
                By.XPATH,
                f"//span[contains(text(), '{section}')]",
            ), f"Section '{section}' not found on results page"

    def wait_for_results_loading(self, timeout: int = 20):
        """
        Wait until the loading indicator disappears.
        """

        logger.info("Waiting for results page to finish loading")

        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((By.TAG_NAME, "circle"))
        )