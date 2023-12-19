from selene import have, be
from allure import step


def test_search(browser_management):
    with step("Открываем сайт Wikipedia"):
        browser = browser_management
        browser.open("/").wait_until(have.title("Wikipedia"))

    with step("Выполняем поиск Bitcoin"):
        browser.element("#searchInput").type("Bitcoin").press_enter()

    with step("Проверяем в выпадающем списке первую запись на соответствие Bitcoin"):
        browser.element(".mw-page-title-main").should(be.visible)