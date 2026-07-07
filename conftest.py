import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

load_dotenv()
DEBUG = True


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    assert url, "BASE_URL is not set in .env"
    return url


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    # options.add_argument("--headless=new")

    if DEBUG:
        options.add_experimental_option("detach", True)
        options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)

    yield driver

    if not DEBUG:
        driver.quit()


@pytest.fixture(autouse=True)
def open_application(driver, base_url):
    driver.get(base_url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "search"))
    )

    # Dismiss cookie consent banner if present
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
    except TimeoutException:
        pass

    # Dismiss version update modal if present
    try:
        WebDriverWait(driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[data-test-id='interactive-frame']")
            )
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "interactive-close-button"))
        ).click()
    except TimeoutException:
        pass
    finally:
        driver.switch_to.default_content()
