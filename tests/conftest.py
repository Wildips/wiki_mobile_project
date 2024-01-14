import allure
import allure_commons
import pytest

from config import session_setup

from selenium import webdriver

from selene import browser, support
from appium import webdriver
from allure import step

from utils import allure


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        required=False,
        default="bstack",
        choices=["local_emulator", "bstack"],
    )


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope="function")
def app_management(context):
    with step("Настраиваем сессию android приложения"):
        options, settings = session_setup(context)
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
