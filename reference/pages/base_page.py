from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def js_click(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click()", el)

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def get_text(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def get_attribute(self, locator, attribute) -> str:
        return self.wait.until(EC.presence_of_element_located(locator)).get_attribute(attribute)

    def wait_for_invisible(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", element)

    def select_react_dropdown(self, locator, value, send_keys=False):
        """
        Interact with a react-select dropdown.
        Use send_keys=True when the field requires typing to filter options.
        Re-fetches element before attribute access to avoid stale references.
        """
        field = self.wait.until(EC.element_to_be_clickable(locator))
        if send_keys:
            field.send_keys(value)
        else:
            field.click()
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'option')]"))
        )
        self.driver.find_element(
            By.XPATH, f"//div[contains(@id,'option') and contains(text(),'{value}')]"
        ).click()

    def dismiss_react_dropdown(self):
        """Press Escape to close any open react-select dropdown."""
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
