import allure
import allure_commons
import pytest
from dotenv import load_dotenv
from config import settings
from selenium import webdriver
from selene import browser, support
from appium import webdriver
from allure import step
from wiki_mobile_tests.utils import allure


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        required=False,
        default="bstack",
        choices=["local_emulator", "bstack"],
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope="function", autouse=True)
def app_management(context):
    with step("Настраиваем сессию android приложения"):
        options = settings.session_setup(context)
        browser.config.driver = webdriver.Remote(settings.url, options=options)
        browser.config.timeout = 10.0
        browser.config._wait_decorator = support._logging.wait_with(
            context=allure_commons._allure.StepContext
        )

        yield browser, settings

    allure.attach_bstack_screenshot()
    allure.attach_bstack_page_source()

    session_id = browser.driver.session_id

    with step("Завершаем сессию android приложения"):
        browser.quit()

    if context == "bstack":
        allure.attach_bstack_video(session_id, settings.login, settings.password)
