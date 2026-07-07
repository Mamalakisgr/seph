from logger import logger
from urllib.parse import unquote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class Homepage(BasePage):
    # Search bar
    SEARCH_BOX           = (By.ID, "search")
    SEARCH_BUTTON        = (By.ID, "varsome-search-btn")
    SEARCH_DROPDOWN_TEXT = (By.CLASS_NAME, "select-selected")

    # Optional Sample Information modal
    SEARCH_MODAL         = (By.CSS_SELECTOR, "[data-testid='modal']")
    SEARCH_MODAL_TITLE   = (By.XPATH, "//div[@data-testid='modal']//div[contains(text(), 'Optional Sample Information')]")
    GERMLINE_BUTTON      = (By.XPATH, "//div[contains(text(), 'Germline')]")
    MODAL_SEARCH_BTN     = (By.XPATH, "//*[@data-testid='modal']//button[.//div[contains(text(), 'Search')]]")

    # Modal fields
    PHENOTYPE_INPUT      = (By.XPATH, "//*[@id='germline-modal-phenotypes']//input[contains(@id,'react-select')]")
    SEX_INPUT            = (By.XPATH, "//*[@id='germline-modal-sex']//input[contains(@id,'react-select')]")
    AGE_ONSET_INPUT      = (By.XPATH, "//*[@id='germline-modal-onset-age']//input[contains(@type,'text')]")
    ETHNICITY_INPUT      = (By.XPATH, "//*[@id='germline-modal-ethnicity']//input[contains(@id,'react-select')]")
    INHERITANCE_INPUT    = (By.XPATH, "//*[@id='germline-modal-inheritance']//input[contains(@id,'react-select')]")
    FM_AFFECTED_INPUT    = (By.XPATH, "//*[@id='germline-modal-family-members-affected']//input[contains(@id,'react-select')]")
    ZYGOSITY_INPUT       = (By.XPATH, "//*[@id='germline-modal-zygosity']//input[contains(@id,'react-select')]")
    SEGREGATION_INPUT    = (By.XPATH, "//*[@id='germline-modal-onset-age'][2]//input[contains(@id,'react-select')]")

    # -----------------------------------------------------------------------

    def verify_loaded(self):
        assert self.is_visible(self.SEARCH_BOX), "Search box is not visible"
        genome_text = self.get_text(self.SEARCH_DROPDOWN_TEXT)
        assert genome_text == "hg38", f"Expected 'hg38', got '{genome_text}'"

    def search_for(self, term: str):
        self.type(self.SEARCH_BOX, term)
        self.click(self.SEARCH_BUTTON)
        assert self.is_visible(self.SEARCH_MODAL), "Search modal did not appear"
        modal_title = self.get_text(self.SEARCH_MODAL_TITLE)
        assert modal_title == "Optional Sample Information", \
            f"Unexpected modal title: '{modal_title}'"

    def fill_sample_information(self, phenotype: str, sex: str, age: str, ethnicity: str):
        germline_class = self.get_attribute(self.GERMLINE_BUTTON, "class")
        assert "tw-bg-primary" in germline_class, "Germline is not selected by default"

        logger.info("Selecting phenotype")
        self.select_react_dropdown(self.PHENOTYPE_INPUT, phenotype, send_keys=True)
        self.dismiss_react_dropdown()

        logger.info("Selecting sex")
        self.select_react_dropdown(self.SEX_INPUT, sex)

        logger.info("Entering age of onset")
        self.type(self.AGE_ONSET_INPUT, age)

        logger.info("Selecting ethnicity")
        self.select_react_dropdown(self.ETHNICITY_INPUT, ethnicity)
        self.dismiss_react_dropdown()

        optional_fields = {
            "Inheritance":             self.INHERITANCE_INPUT,
            "Family Members Affected": self.FM_AFFECTED_INPUT,
            "Zygosity":                self.ZYGOSITY_INPUT,
            "Family Segregation":      self.SEGREGATION_INPUT,
        }
        for field_name, locator in optional_fields.items():
            logger.info(f"  Checking {field_name} is empty")
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(locator))
            assert self.driver.find_element(*locator).get_attribute("value") == "", \
                f"{field_name} field should be empty"

    def submit_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.MODAL_SEARCH_BTN)
        ).click()
