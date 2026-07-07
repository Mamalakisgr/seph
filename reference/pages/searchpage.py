from logger import logger
from urllib.parse import unquote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class SearchPage(BasePage):
    # Results page
    CARD_CONTAINER     = (By.ID, "card-container")
    LOADER             = (By.CSS_SELECTOR, "circle")

    # ACMG / Germline Classification section
    ACMG_SECTION       = (By.CSS_SELECTOR, "div.varsome-result-fixed.cmpt_acmg")
    VERDICT_PILL       = (By.CSS_SELECTOR, "span.saph-pill")
    ACMG_SCORES        = (By.CSS_SELECTOR, "[data-testid='ACMG_scores']")
    AUTOMATED_CRITERIA = (By.XPATH, ".//h5[contains(text(),'Automated criteria')]")

    # Security / bot-check page
    PROCEED_BTN        = (By.ID, "proceedBtn")

    EXPECTED_SECTIONS = [
        "General Information",
        "Germline Classification",
        "PharmGKB",
        "ClinVar",
        "LOVD",
        "Publications",
    ]

    # -----------------------------------------------------------------------

    def handle_security_page(self, search_term: str):
        WebDriverWait(self.driver, 10).until(
            lambda d: search_term in unquote(d.current_url) or d.find_elements(*self.PROCEED_BTN)
        )
        if self.driver.find_elements(*self.PROCEED_BTN):
            logger.info("  Security page detected – clicking proceedBtn")
            self.driver.find_element(*self.PROCEED_BTN).click()
            WebDriverWait(self.driver, 10).until(
                lambda d: search_term in unquote(d.current_url)
            )
        assert search_term in unquote(self.driver.current_url), \
            f"Expected '{search_term}' in URL, got: {self.driver.current_url}"

    def wait_for_page_load(self):
        self.wait_for_invisible(self.LOADER)

    def verify_sections_present(self):
        for section in self.EXPECTED_SECTIONS:
            logger.info(f"  Checking section: {section}")
            assert self.driver.find_elements(
                By.XPATH, f"//span[contains(normalize-space(), '{section}')]"
            ), f"Section '{section}' not found on results page"

    def get_germline_card(self):
        card = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@class,'card') and .//*[contains(text(),'Germline Classification')]]")
            )
        )
        assert card.is_displayed(), "Germline Classification card is not visible"
        return card

    def expand_and_verify_germline_classification(self, germline_card):
        expand_btn = germline_card.find_element(
            By.XPATH, ".//*[contains(text(),'Germline Classification')]"
        )
        self.driver.execute_script("arguments[0].click()", expand_btn)

        acmg_section = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ACMG_SECTION)
        )
        self.scroll_into_view(acmg_section)

        verdict = acmg_section.find_element(*self.VERDICT_PILL)
        assert verdict.is_displayed(), "Classification verdict pill is not visible"
        logger.info(f"  Classification verdict: {verdict.text}")

        acmg_scores = acmg_section.find_element(*self.ACMG_SCORES)
        assert acmg_scores.is_displayed(), "ACMG scores are not visible"

        automated_criteria = acmg_section.find_element(*self.AUTOMATED_CRITERIA)
        assert automated_criteria.is_displayed(), "Automated criteria table is not visible"
