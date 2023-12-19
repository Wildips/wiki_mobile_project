from selene import have
from allure import step


def test_search(browser_management):
    with step("Открываем сайт Wikipedia"):
        browser = browser_management
        browser.open("/").wait_until(have.title("Wikipedia"))

    with step("Выполняем поиск Appium"):
        browser.element("#searchInput").type("Appium")

    with step("Проверяем в выпадающем списке первую запись на соответствие Appium"):
        results = browser.all(".suggestion-link")
        results.should(have.size_greater_than(0))
        results.first.should(have.text("Appium"))
