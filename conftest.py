import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture
def setup(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    driver = None

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError("Browser option must be 'chrome' or 'firefox'")

    driver.maximize_window()
    request.node.driver = driver  # Attach driver to the request node for access in hooks

    yield driver
    driver.quit()


# Hook to take screenshot on failure and attach to Allure report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Only act on actual test calls, and only if it failed
    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
