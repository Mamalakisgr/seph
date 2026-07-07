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
    GERMLINE_CLASSIFICATION_SECTION = (By.XPATH, "//a[contains(text(),'Germline Variant Classification')]")
    CLASSIFICATION_VERDICT_PILL = (By.XPATH, "//*[@id='components-start']//div[contains(@class,'saph-pill')]")
    AUTOMATED_CRITERIA_HEADER = (By.XPATH, "//*[@id='components-start']//h5[contains(text(),'Automated criteria')]")    

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

    def verify_automated_criteria_displayed(self):
        logger.info("Verifying automated criteria table is displayed")
        assert self.is_element_visible(self.AUTOMATED_CRITERIA_HEADER), ("Automated criteria table is not visible")
    
    def verify_classification_verdict(self, expected_text="Pathogenic", expected_rgb=None):
        logger.info("Verifying classification verdict is displayed")
        pill = self.wait.until(EC.visibility_of_element_located(self.CLASSIFICATION_VERDICT_PILL))

        actual_text = pill.find_element(By.TAG_NAME, "span").text
        logger.info(f"Classification verdict: {actual_text}")
        assert actual_text == expected_text, f"Unexpected classification verdict: {actual_text}"

        if expected_rgb:
            actual_color = pill.value_of_css_property("background-color")
            expected_rgba = expected_rgb.replace("rgb(", "rgba(").rstrip(")") + ", 1)"
            logger.info(f"Verdict background-color: {actual_color}")
            assert actual_color in (expected_rgb, expected_rgba), (
                f"Expected verdict color '{expected_rgb}', got '{actual_color}'"
            )    