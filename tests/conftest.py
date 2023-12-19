import allure
import allure_commons
import pytest
import config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# from selene.support.shared import browser
from selene import browser, support
from appium import webdriver
from allure import step

from utils import attach, allure

DEFAULT_BROWSER_VERSION = "100.0"


def pytest_addoption(parser):
    parser.addoption("--browser-version", default=DEFAULT_BROWSER_VERSION)


@pytest.fixture(scope="function")
def browser_management(request):
    with step("Настраиваем web браузер"):
        browser_version = request.config.getoption("--browser-version")
        browser_version = (
            browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
        )
        options = Options()
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {"enableVNC": True, "enableVideo": True},
        }
        options.capabilities.update(selenoid_capabilities)

        driver = webdriver.Remote(
            command_executor=f"https://{config.SELENOID_USER}:{config.SELENOID_USER_PASSWORD}@selenoid.autotests.cloud/wd/hub",
            options=options,
        )
        browser.config.driver = driver

        # browser.config.base_url = config.TEST_WEB_BROWSER_URL
        browser.config.base_url = "https://www.wikipedia.org"
        # browser.config.driver_name = os.getenv("driver_name", "chrome")

        # coach example:
        # from selenium import webdriver
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser.config.driver_options = chrome_options

        # browser.config.hold_driver_at_exit = (
        #     os.getenv("hold_driver_at_exit", "false").lower() == "true"
        # )
        browser.config.window_width = 1920  # os.getenv("window_width", "1920")
        browser.config.window_height = 1080  # os.getenv("window_height", "1080")
        browser.config.timeout = 4.0  # float(os.getenv("timeout", "4.0"))

        yield browser

        attach.add_html(browser)
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_video(browser)

        browser.quit()


@pytest.fixture(scope="function")
def android_mobile_management():
    options = UiAutomator2Options().load_capabilities(
        {
            # Specify device and os_version for testing
            # 'platformName': 'android',
            "platformVersion": "9.0",
            "deviceName": "Google Pixel 3",
            # Set URL of the application under test
            "app": "bs://sample.app",
            # Set other BrowserStack capabilities
            "bstack:options": {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",
                # Set your access credentials
                "userName": config.LOGIN_MOBILE,
                "accessKey": config.PASSWORD_MOBILE,
            },
        }
    )

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options

    with step("Настраиваем сессию android приложения"):
        browser.config.driver = webdriver.Remote(
            config.REMOTE_MOBILE_URL, options=options
        )
        browser.config.timeout = 10.0  # float(os.getenv("timeout", "10.0"))
        browser.config._wait_decorator = support._logging.wait_with(
            context=allure_commons._allure.StepContext
        )

    yield browser

    allure.attach_bstack_screenshot()
    allure.attach_bstack_page_source()

    session_id = browser.driver.session_id

    with step("Завершаем сессию android приложения"):
        browser.quit()

    allure.attach_bstack_video(session_id)


@pytest.fixture(scope="function")
def ios_mobile_management():
    options = XCUITestOptions().load_capabilities(
        {
            # Specify device and os_version for testing
            "platformName": "ios",
            "platformVersion": "16",
            "deviceName": "iPhone 14",
            # Set URL of the application under test
            "app": "bs://444bd0308813ae0dc236f8cd461c02d3afa7901d",
            # Set other BrowserStack capabilities
            "bstack:options": {
                "projectName": "Ios tests",
                "buildName": "browserstack-simple-app-build",
                "sessionName": "BStack Simple app test",
                # Set your access credentials
                "userName": config.LOGIN_MOBILE,
                "accessKey": config.PASSWORD_MOBILE,
            },
        }
    )

    with step("Настраиваем сессию ios приложения"):
        browser.config.driver = webdriver.Remote(
            config.REMOTE_MOBILE_URL, options=options
        )
        browser.config.timeout = 10.0  # float(os.getenv("timeout", "10.0"))
        browser.config._wait_decorator = support._logging.wait_with(
            context=allure_commons._allure.StepContext
        )

    yield

    allure.attach_bstack_screenshot()
    allure.attach.attach_bstack_page_source()

    session_id = browser.driver.session_id

    with step("Завершаем сессию ios приложения"):
        browser.quit()

    allure.attach_bstack_video(session_id)
