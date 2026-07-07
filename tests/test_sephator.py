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

    logger.info("Navigating to the homepage")
    assert driver.current_url == "https://varsome.com/"
    search_box_placeholder = home.get_attribute(home.SEARCH_BOX, "placeholder")
    # assert search_box_placeholder == "“Enter gene, transcript, variant, or region."

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

    # Complete the Optional Sample Information Modal
    germline_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Germline')]")
    assert "tw-bg-primary" in germline_button.get_attribute("class"), "Germline button is not selected by default"
    
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
    

    # Proceed to the search results page
    logger.info("Clicking the 'Search' button to proceed to the search results page")
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@data-testid='modal']//button[.//div[contains(text(), 'Search')]]"))
    )
    time.sleep(0.5)
    button.click()

    # Security page handling and final assertion for search results page
    logger.info("Waiting for the search results page to load and checking the URL")
    searchpage = SearchPage(driver)

    searchpage.handle_security_page(
    expected_url_text="BRAF:V600E"
    )

    # Search Page Assertions
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

    searchpage.scroll_into_view(searchpage.WARNING_BUTTON)
    searchpage.click(searchpage.WARNING_BUTTON)

    germline_classification_section = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//a[contains(text(),'Germline Variant Classification')]")
        )
    )

    # searchpage.scroll_into_view(germline_classification_section)
    # assert germline_classification_section.is_displayed(), "Germline Variant Classification section is not visible after expanding"
    
    logger.info("Verifying classification verdict is displayed")
    components_section = driver.find_element(By.ID, "components-start")
    verdict = components_section.find_element(By.CSS_SELECTOR, "div.saph-pill")
    assert verdict.is_displayed(), "Classification verdict pill is not visible"
    logger.info(f"Classification verdict: {verdict.text}")
    assert verdict.text == "Pathogenic", f"Unexpected classification verdict: {verdict.text}"
    expected_rgb="rgb(199, 7, 0)"
    actual_rgb = verdict.value_of_css_property("background-color")
    assert actual_rgb == expected_rgb, f"Expected background color {expected_rgb}, but got {actual_rgb}"
    logger.info("Verifying automated criteria table is displayed")
    assert germline_classification_section.find_element(By.XPATH, ".//h5[contains(text(),'Automated criteria')]").is_displayed(), "Automated criteria table is not visible"