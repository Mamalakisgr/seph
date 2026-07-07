from pages.init_page import InitPage
from selenium.webdriver.common.by import By

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
    AGE_ONSET_INPUT = (By.XPATH, "//*[@id='germline-modal-onset-age']//input[contains(@id,'react-select')]")
    ETHNICITY_INPUT = (By.XPATH, "//*[@id='germline-modal-ethnicity']//input[contains(@id,'react-select')]")