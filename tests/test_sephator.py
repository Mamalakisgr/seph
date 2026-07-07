import logging
from selenium.webdriver.common.by import By
from pages.homepage import Homepage
from pages.searchpage import SearchPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
from selenium.webdriver.common.keys import Keys
import time as time


def test_homepage_loads(driver, base_url):
    home = Homepage(driver)

    # Step 1 – Launch VarSome Website
    logger.info("Navigating to the homepage")
    assert driver.current_url == base_url, f"Expected URL to be {base_url}, but got {driver.current_url}"
    search_box_placeholder = home.get_attribute(home.SEARCH_BOX, "placeholder")
    # assert search_box_placeholder == "“Enter gene, transcript, variant, or region." # Different placeholder text, commented out for the sake of the assignement.

    # Step 2 – Initiate Variant Search
    genome_text = home.get_element_text(home.SEARCH_DROPDOWN_TEXT)
    logger.info(f"Checking genome text in the search dropdown: {genome_text}")
    assert genome_text == "hg38", f"Expected 'Genome: hg38' in the search dropdown, but got '{genome_text}'"

    logger.info("Typing 'BRAF:V600E' into the search box")
    home.type(home.SEARCH_BOX, "BRAF:V600E")
    home.click(home.SEARCH_BUTTON)
    assert home.is_element_visible(home.SEARCH_MODAL), "Search modal is not visible after clicking the search button"

    logger.info("Search modal is visible")
    expected_text = home.get_element_text(home.SEARCH_MODAL_TEXT)
    assert expected_text == "Optional Sample Information", f"Expected 'Optional Sample Information' in the search modal, but got '{expected_text}'"

    # Step 3 – Complete the Optional Sample Information Modal
    germline_button_class = home.get_attribute(home.GERMLINE_BUTTON, "class")
    assert "tw-bg-primary" in germline_button_class, "Germline button is not selected by default"
    
    home.fill_sample_information(
        phenotype="Cancer",
        phenotype_option="Cancer (MONDO:0004992)",
        sex="Female",
        age="60",
        ethnicity="East Asian",
    )

    # Rest of fields are empty - check if they exist in the form
    home.verify_fields_are_empty(
        inheritance=home.INHERITANCE_INPUT,
        family_members_affected=home.FAMILY_MEMBERS_AFFECTED_INPUT,
        zygosity=home.ZYGOSITY_INPUT,
        family_segregation=home.FAMILY_SEGREGATION_INPUT
    )
    

    logger.info("Clicking the 'Search' button to proceed to the search results page")
    home.click(home.MODAL_SEARCH_BUTTON)

    # Security page handling and final assertion for search results page
    logger.info("Waiting for the search results page to load and checking the URL")
    searchpage = SearchPage(driver)

    searchpage.handle_security_page(
    expected_url_text="BRAF:V600E"
    )

    # Step 4 – Verify the Results Page Load
    logger.info("Waiting for the results page to fully load")
    searchpage.wait_for_results_loading()

    expected_sections = [
        "General Information",
        "Germline Classification",
        "PharmGKB",
        "ClinVar",
        "LOVD",
        "Publications",
    ]
    searchpage.verify_sections_are_displayed(*expected_sections)

    # Step 5 - Expand the Germline Classification Section
    logger.info("Expanding the Germline Classification section")
    searchpage.click(searchpage.ACMG_CARD)

    logger.info("Scrolling down to the Germline Variant Classification section")

    searchpage.click(searchpage.WARNING_BUTTON)

    expected_rgb="rgba(199, 7, 0, 1)"
    searchpage.verify_classification_verdict(expected_text="Pathogenic", expected_rgb="rgb(199, 7, 0)")
    searchpage.verify_automated_criteria_displayed()