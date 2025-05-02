import allure
from selene import browser, have


def test_auth():
    with allure.step("Проверка авторизации"):
        browser.open("home")
        assert browser.element('[class="flex company"]').should(have.text('ООО Март'))