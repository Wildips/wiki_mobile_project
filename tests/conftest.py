import allure
import allure_commons
import pytest
from config import settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# from selene.support.shared import browser
from selene import browser, support
from appium import webdriver
from allure import step

from utils import attach, allure

DEFAULT_BROWSER_VERSION = "100.0"
DEFAULT_LOCAL_BROWSER_VERSION = "119.0"
DEFAULT_BROWSER_NAME = "chrome"


def pytest_addoption(parser):
    parser.addoption("--browser-version", default=DEFAULT_BROWSER_VERSION)


@pytest.fixture(scope="function")
def browser_management(request):
    with step("Настраиваем web браузер"):
        browser_version = request.config.getoption("--browser-version")
        if DEFAULT_BROWSER_NAME == "chrome":
            browser_version = (
                browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
            )
        elif DEFAULT_BROWSER_NAME == "firefox":
            browser_version = "119.0"

        if DEFAULT_BROWSER_NAME == "chrome":
            options = ChromeOptions()
        elif DEFAULT_BROWSER_NAME == "chrome":
            options = FirefoxOptions()

        if settings.context == "remote":
            selenoid_capabilities = {
                "browserName": DEFAULT_BROWSER_NAME,
                "browserVersion": browser_version,
                "selenoid:options": {"enableVNC": True, "enableVideo": True},
            }
            options.capabilities.update(selenoid_capabilities)

            driver = webdriver.Remote(
                command_executor=f"https://{settings.selenoid_user}:{settings.selenoid_user_password}@selenoid.autotests.cloud/wd/hub",
                options=options,
            )
            browser.config.driver = driver

        browser.config.base_url = "https://www.wikipedia.org"

        # coach example:
        # from selenium import webdriver
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser.config.driver_options = chrome_options

        # coach example:
        # browser.config.hold_driver_at_exit = (
        #     os.getenv("hold_driver_at_exit", "false").lower() == "true"
        # )

        browser.config.window_width = 1920
        browser.config.window_height = 1080
        browser.config.timeout = 4.0

        yield browser

        attach.add_html(browser)
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_video(browser)

        browser.quit()


@pytest.fixture(scope="function")
def android_app_management():
    options = UiAutomator2Options()
    with step("Настраиваем сессию android приложения"):
        if settings.context == "remote":
            options.load_capabilities(
                {
                    # Specify device and os_version for testing
                    "platformName": settings.mobile_os,
                    "platformVersion": "9.0",
                    "deviceName": "Google Pixel 3",
                    # Set URL of the application under test
                    "app": settings.browserstack_app,
                    # Set other BrowserStack capabilities
                    "bstack:options": {
                        "projectName": "Android app tests",
                        "buildName": "browserstack-build-1",
                        "sessionName": "BStack first_test",
                        # Set your access credentials
                        "userName": settings.login_mobile,
                        "accessKey": settings.password_mobile,
                    },
                }
            )

            browser.config.driver = webdriver.Remote(
                settings.remote_mobile_url, options=options
            )
            browser.config.timeout = 10.0  # float(os.getenv("timeout", "10.0"))
            browser.config._wait_decorator = support._logging.wait_with(
                context=allure_commons._allure.StepContext
            )

        elif settings.context == "local_emulator":
            # options.set_capability("platform_name", "android")
            options.set_capability("app", settings.local_emulator_app)
            options.set_capability("udid", "emulator-5554")
            options.set_capability("appWaitActivity", settings.app_wait_activity)
            # options.set_capability("remote_url", settings.local_mobile_url)

            browser.config.driver = webdriver.Remote(
                settings.local_mobile_url, options=options
            )
            browser.config.timeout = 10.0  # float(os.getenv("timeout", "10.0"))
            browser.config._wait_decorator = support._logging.wait_with(
                context=allure_commons._allure.StepContext
            )

        elif settings.context == "local_real":
            ...
            # for example (for realization)
            # options.set_capability("app", "")
            # options.set_capability("udid", "")
            # options.set_capability("appWaitActivity", Settings.app_wait_activity)
            # options.set_capability("remote_url", "")

            # browser.config.driver = webdriver.Remote("", options=options)
            # browser.config.timeout = 10.0  # float(os.getenv("timeout", "10.0"))
            # browser.config._wait_decorator = support._logging.wait_with(
            #     context=allure_commons._allure.StepContext
            # )

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options

    yield browser

    allure.attach_bstack_screenshot()
    allure.attach_bstack_page_source()

    session_id = browser.driver.session_id

    with step("Завершаем сессию android приложения"):
        browser.quit()

    if settings.context == "remote":
        allure.attach_bstack_video(session_id)


@pytest.fixture(scope="function")
def ios_app_management():
    options = XCUITestOptions()
    if settings.context == "remote":
        options.load_capabilities(
            {
                # Specify device and os_version for testing
                "platformName": settings.mobile_os,
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
                    "userName": settings.login_mobile,
                    "accessKey": settings.password_mobile,
                },
            }
        )
    elif settings.context == "local_emulator":
        ...

    elif settings.context == "local_real":
        ...

    with step("Настраиваем сессию ios приложения"):
        browser.config.driver = webdriver.Remote(
            settings.remote_mobile_url, options=options
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

    if settings.context == "remote":
        allure.attach_bstack_video(session_id)
