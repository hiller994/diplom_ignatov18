import allure
from selene import browser, have

def test_create_driver():
    with allure.step("Cоздания водителя"):
        browser.open("drivers?tab=0")
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Введите фамилию"]').type('Автотестов')
        browser.element('[placeholder = "Введите имя"]').type('Водитель')
        browser.element('[placeholder="Введите отчество"]').type('Тест')
        browser.element('[placeholder = "Введите номер телефона"]').type('72328280416')
        browser.element('[placeholder="Введите примечание"]').type('Создание через автотест')
        browser.element('[class ="btn btn--green"]').click()
        browser.element('[class="c-red"]').click()
        browser.element('[class="table__item"]').should(have.text('Автотестов'))
