from logger import logger
from selenium.webdriver.common.by import By
from pages.homepage import Homepage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote
import time as time

# def test_homepage_(driver):
#     home = Homepage(driver)
#     logger.info("Navigating to the homepage")
#     assert driver.current_url == "https://varsome.com/"
#     search_box_placeholder = driver.find_element(By.ID, home.SEARCH_BOX).get_attribute("placeholder")
#     assert search_box_placeholder == "Search for variants, CNVs, genes, transcripts, publications, diseases..."


def test_homepage_loads(driver, base_url):
    home = Homepage(driver)

    logger.info("Checking search box visibility and functionality")
    assert home.is_element_visible(home.SEARCH_BOX), "Search box is not visible on the homepage"

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
    
    # Select the "Cancer" option in the Phenotype field
    logger.info("Selecting 'Cancer' in the Phenotype field")
    phenotype_field = driver.find_element(By.XPATH, "//*[@id='germline-modal-phenotypes']//input[contains(@id,'react-select')]")
    phenotype_field.send_keys("Cancer")
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'option')]"))
    )
    home.select_modal_option("germline-modal-phenotypes", "Cancer (MONDO:0004992)")
    germline_button.click()  
    
    # Select "Female" option the Sex field
    logger.info("Selecting 'Female' in the Sex field")
    sex_field = driver.find_element(By.XPATH, "//*[@id='germline-modal-sex']//input[contains(@id,'react-select')]")
    sex_field.click()
    home.select_modal_option("germline-modal-sex", "Female")

    # Select "60" in the Age of Onset field
    logger.info("Selecting '60' in the Age of Onset field")
    age_onset_field = driver.find_element(By.XPATH, "//*[@id='germline-modal-onset-age']//input[contains(@type,'text')]")
    age_onset_field.send_keys("60")

    logger.info("Selecting 'East Asian' in the Ethnicity field")
    ethnicity_field = driver.find_element(By.XPATH, "//*[@id='germline-modal-ethnicity']//input[contains(@id,'react-select')]")
    ethnicity_field.click()
    home.select_modal_option("germline-modal-ethnicity", "East Asian")
    # option = driver.find_element(By.XPATH, "//div[contains(@id,'option') and contains(text(),'East Asian')]")
    # option.click()
    germline_button.click()
    # ethnicity_field.send_keys(Keys.ESCAPE)

    # Rest of fields are empty - check if they exist in the form
    optional_fields = {
        "Inheritance": "//*[@id='germline-modal-inheritance']//input[contains(@id,'react-select')]",
        "Family Members Affected": "//*[@id='germline-modal-family-members-affected']//input[contains(@id,'react-select')]",
        "Zygosity": "//*[@id='germline-modal-zygosity']//input[contains(@id,'react-select')]",
        "Family Segregation": "//*[@id='germline-modal-onset-age'][2]//input[contains(@id,'react-select')]"
    }
    
    for field_name, xpath in optional_fields.items():
        logger.info(f"Checking {field_name} field")
        field = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        assert field.get_attribute("value") == "", f"{field_name} field is not empty"

    # Proceed to the search results page
    logger.info("Clicking the 'Search' button to proceed to the search results page")
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@data-testid='modal']//button[.//div[contains(text(), 'Search')]]"))
    )
    time.sleep(0.5)
    button.click()

    # Security page handling and final assertion for search results page
    logger.info("Waiting for the search results page to load and checking the URL")
    WebDriverWait(driver, 10).until(
        lambda d: "BRAF:V600E" in unquote(d.current_url) or d.find_elements(By.ID, "proceedBtn")
    )
    if driver.find_elements(By.ID, "proceedBtn"):
        logger.info("Security page detected, clicking proceedBtn")
        driver.find_element(By.ID, "proceedBtn").click()
        WebDriverWait(driver, 10).until(
            lambda d: "BRAF:V600E" in unquote(d.current_url)
        )
    assert "BRAF:V600E" in unquote(driver.current_url)
    logger.info(f"Search results page loaded successfully with URL: {driver.current_url}")

    # Search Page Assertions
    logger.info("Waiting for the results page to fully load")
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "circle"))
    )

    expected_sections = [
        "General Information",
        "Germline Classification",
        "PharmGKB",
        "ClinVar",
        "LOVD",
        "Publications",
    ]
    for section in expected_sections:
        logger.info(f"Checking section: {section}")
        assert driver.find_elements(
            By.XPATH, f"//span[contains(text(), '{section}')]"
        ), f"Section '{section}' not found on results page"

    logger.info("Checking Germline Classification card is visible in the top panel")
    germline_card = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='variantDetails' and .//span[normalize-space()='Germline Classification']]"))
    )
    assert germline_card.is_displayed(), "Germline Classification card is not visible"

    # # # Step 5 - Expand the Germline Classification Section
    # logger.info("Expanding the Germline Classification section")
    # expand_btn = germline_card.find_element(By.CSS_SELECTOR, "[data-testid='acmg']")
    # expand_btn.click()

    # logger.info("Scrolling down to the Germline Variant Classification section")
    # germline_classification_section = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located(
    #         (By.XPATH, "//*[contains(text(),'Germline Variant Classification')]")
    #     )
    # )
    # germline_classification_section.scroll_into_view()
    # assert germline_classification_section.is_displayed(), "Germline Variant Classification section is not visible after expanding"
    
    # logger.info("Verifying classification verdict is displayed")
    # verdict = germline_classification_section.find_element(By.CSS_SELECTOR, "span.saph-pill")
    # assert verdict.is_displayed(), "Classification verdict pill is not visible"
    # logger.info(f"Classification verdict: {verdict.text}")

    # logger.info("Verifying ACMG scores are displayed")
    # acmg_scores_section = germline_classification_section.find_element(By.CSS_SELECTOR, "[data-testid='ACMG_scores']")
    # acmg_scores = acmg_scores_section.find_element(By.CSS_SELECTOR, "[data-testid='ACMG_scores']")
    # assert acmg_scores.is_displayed(), "ACMG scores are not visible"

    # logger.info("Verifying automated criteria table is displayed")
    # assert germline_classification_section.find_element(By.XPATH, ".//h5[contains(text(),'Automated criteria')]").is_displayed(), "Automated criteria table is not visible"