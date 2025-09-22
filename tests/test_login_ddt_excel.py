import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.excel_utils import read_test_data

# Read test data from Excel
test_data = read_test_data("test_data/login_data.xlsx")

@pytest.mark.parametrize("data", test_data)
def test_login_ddt_excel(setup, data):
    driver = setup
    driver.get("https://practicetestautomation.com/practice-test-login/")

    login_page = LoginPage(driver)
    login_page.enter_username(data["username"])
    login_page.enter_password(data["password"])
    login_page.click_login()

    if data["expected"] == "success":
        home_page = HomePage(driver)
        assert "Logged In Successfully" in home_page.get_success_message()
        assert home_page.is_logout_button_visible()
    else:
        # Add a small wait to ensure error message loads
        import time
        time.sleep(1)  # Wait for error message to appear
        
        # Try different selectors for the error message
        error_selectors = [
            "id=error",
            "css selector=.error",
            "css selector=#error",
            "xpath=//div[@id='error']"
        ]
        
        error_text = ""
        for selector in error_selectors:
            try:
                if "id=" in selector:
                    error_text = driver.find_element("id", selector.split("=")[1]).text
                elif "css selector=" in selector:
                    error_text = driver.find_element("css selector", selector.split("=")[1]).text
                elif "xpath=" in selector:
                    error_text = driver.find_element("xpath", selector.split("=")[1]).text
                if error_text:
                    break
            except:
                continue
        
        print(f"Error text found: '{error_text}'")  # Debug output
        assert error_text, "Error message should not be empty for failed login"
        assert "invalid" in error_text.lower() or "incorrect" in error_text.lower()