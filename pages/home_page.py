from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.success_message = (By.TAG_NAME, "h1")
        self.logout_button = (By.LINK_TEXT, "Log out")

    def get_success_message(self):
        return self.driver.find_element(*self.success_message).text

    def is_logout_button_visible(self):
        return self.driver.find_element(*self.logout_button).is_displayed()
