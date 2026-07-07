import logging
from pages.init_page import InitPage
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class Homepage(InitPage):
    SEARCH_BOX = (By.ID, "search")
    SEARCH_BUTTON = (By.ID, "varsome-search-btn")
    SEARCH_DROPDOWN_TEXT = (By.CLASS_NAME, "select-selected")
    SEARCH_MODAL = (By.CSS_SELECTOR, "[data-testid='modal']")
    SEARCH_MODAL_TEXT = (By.XPATH, "//div[@data-testid='modal']//div[contains(text(), 'Optional Sample Information')]")
    GERMLINE_BUTTON = (By.XPATH, "//div[contains(text(), 'Germline')]")
    MODAL_SEARCH_BUTTON = (By.XPATH, "//*[@data-testid='modal']//button[.//div[contains(text(), 'Search')]]")
    PHENOTYPE_INPUT = (By.XPATH, "//*[@id='germline-modal-phenotypes']//input[contains(@id,'react-select')]")
    SEX_INPUT = (By.XPATH, "//*[@id='germline-modal-sex']//input[contains(@id,'react-select')]")
    AGE_ONSET_INPUT = (By.XPATH, "//*[@id='germline-modal-onset-age']//input[contains(@type,'text')]")
    ETHNICITY_INPUT = (By.XPATH, "//*[@id='germline-modal-ethnicity']//input[contains(@id,'react-select')]")
    INHERITANCE_INPUT = (By.XPATH, "//*[@id='germline-modal-inheritance']//input[contains(@id,'react-select')]")
    FAMILY_MEMBERS_AFFECTED_INPUT = (By.XPATH, "//*[@id='germline-modal-family-members-affected']//input[contains(@id,'react-select')]")
    ZYGOSITY_INPUT = (By.XPATH, "//*[@id='germline-modal-zygosity']//input[contains(@id,'react-select')]")
    FAMILY_SEGREGATION_INPUT = (By.XPATH, "//*[@id='germline-modal-onset-age'][2]//input[contains(@id,'react-select')]")

    def fill_sample_information(self, phenotype: str = None, sex: str = None, age: str = None, ethnicity: str = None, phenotype_option: str = None):
        germline_class = self.get_attribute(self.GERMLINE_BUTTON, "class")
        assert "tw-bg-primary" in germline_class, "Germline is not selected by default"

        logger.info("Selecting phenotype")
        self.select_react_dropdown(self.PHENOTYPE_INPUT, phenotype_option or phenotype, send_keys=True, search_text=phenotype)
        self.click(self.GERMLINE_BUTTON)

        logger.info("Selecting sex")
        self.select_react_dropdown(self.SEX_INPUT, sex)

        logger.info("Entering age of onset")
        self.type(self.AGE_ONSET_INPUT, age)

        logger.info("Selecting ethnicity")
        self.select_react_dropdown(self.ETHNICITY_INPUT, ethnicity)
        self.click(self.GERMLINE_BUTTON)