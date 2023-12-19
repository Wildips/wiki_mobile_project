import pytest
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import have, be


@pytest.mark.parametrize("search_text", ["Appium", "Bitcoin"])
def test_search(android_mobile_management, search_text):
    with step("Вводим искомый текст"):
        browser = android_mobile_management
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type(
            search_text
        )

    with step("Проверяем результат"):
        results = browser.all(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        )
        results.should(have.size_greater_than(0))
        results.first.should(have.text(search_text))


@pytest.mark.parametrize("search_text", ["Appium", "Bitcoin"])
def test_click_to_search_result(android_mobile_management, search_text):
    with step("Вводим искомый текст"):
        browser = android_mobile_management
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type(
            search_text
        )
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        ).click()

    with step("Проверяем результат"):
        browser.element((AppiumBy.ACCESSIBILITY_ID, search_text))
