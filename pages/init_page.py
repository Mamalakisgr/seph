from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class InitPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def get_element_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def select_modal_option(self, field_id, value):
        """Select option in react-select field within modal"""
        field = self.driver.find_element(By.XPATH, f"//*[@id='{field_id}']//input[contains(@id,'react-select')]")
        field.click()
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'option')]"))
        )
        option = self.driver.find_element(By.XPATH, f"//div[contains(@id,'option') and contains(text(),'{value}')]")
        option.click()