import pytest
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import have


@pytest.mark.parametrize("search_text", ["Appium", "Bitcoin"])
def test_search(android_app_management, search_text):
    browser = android_app_management
    with step("Пропускаем приветствие"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
        ).click()

    with step("Вводим искомый текст"):
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
def test_click_to_search_result(android_app_management, search_text):
    browser = android_app_management
    with step("Пропускаем приветствие"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
        ).click()

    with step("Вводим искомый текст"):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type(
            search_text
        )
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        ).click()

    with step("Проверяем результат"):
        browser.element((AppiumBy.ACCESSIBILITY_ID, search_text))


def test_wikipedia_getting_started_onboarding_screen(android_app_management):
    browser = android_app_management
    with step("Проверяем приветственный текст"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(
            have.text("The Free Encyclopedia")
        )

    with step("Нажимаем продолжить"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")
        ).click()

    with step("Проверяем открытие второй страницы"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(
            have.exact_text("New ways to explore")
        )

    with step("Нажимаем продолжить"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")
        ).click()

    with step("Проверяем открытие второй страницы"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(
            have.exact_text("Reading lists with sync")
        )

    with step("Нажимаем продолжить"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")
        ).click()

    with step("Проверяем открытие третьей страницы"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(
            have.exact_text("Send anonymous data")
        )

    with step("Отказываемся отправлять данный"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/rejectButton")).click()

    with step("Проверяем что находимся на странице поиска"):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
