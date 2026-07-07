from pages.homepage import Homepage
from pages.searchpage import SearchPage

SEARCH_TERM = "BRAF:V600E"


def test_braf_v600e_germline_classification(driver, base_url):
    home = Homepage(driver)
    search = SearchPage(driver)

    home.verify_loaded()
    home.search_for(SEARCH_TERM)
    home.fill_sample_information(
        phenotype="Cancer (MONDO:0004992)",
        sex="Female",
        age="60",
        ethnicity="East Asian",
    )
    home.submit_modal()

    search.handle_security_page(SEARCH_TERM)
    search.wait_for_page_load()
    search.verify_sections_present()
    germline_card = search.get_germline_card()
    search.expand_and_verify_germline_classification(germline_card)
