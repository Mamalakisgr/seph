from pages.init_page import InitPage
from selenium.webdriver.common.by import By

class SearchPage(InitPage):
    SEARCH_BOX_ID = "search"
    SEARCH_BUTTON_ID = "varsome-search-btn"
    SEARCH_DROPDOWN_CLASS = "select-selected"
    SEARCH_MODAL = "[data-testid='modal']"