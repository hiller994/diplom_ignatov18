import time

import allure
from selene import browser, have

def test_create_driver():
    with allure.step("Cоздания автомобиля"):
        browser.open("transports")
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Введите марку"]').type("Автотест-марка")
        browser.element('[placeholder="Введите модель"]').type("Автотест-модель")
        browser.element('[class="select"]').click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "Россия")]').click()
        #browser.element('[class="input-wrapper"]').click()
        time.sleep(1)
        #browser.element('[class="input-wrapper"]').type('М658716')
        #browser.element('[placeholder=""]').type('М658716')
        browser.element('//*[@id="app"]/div/main/div[4]/div[2]/div/div[1]/div[4]/div[2]/input').type('М719ММ716')
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="table__content__item"]').should(have.text('Автотест-марка'))

