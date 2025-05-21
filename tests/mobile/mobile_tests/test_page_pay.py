import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be


def test_page_pay(mobile_management):
    with allure.step('Поиск АЗС'):
        browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/search_btn")).click()
        browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/search")).type("28")
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/title" and @text="АЗС №28"]')).click()

    with allure.step('Проврека открытия формы АЗС и отображение кнопки заправки'):
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/address" and @text="г. Москва, ул. Рябиновая, д. 12"]')).should(be.visible)
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/fill_online_btn" and @text="Заправиться онлайн"]')).should(
            be.visible)
    with allure.step('Переход на форму формирования заказа'):
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/fill_online_btn" and @text="Заправиться онлайн"]')).click()
        with allure.step('Выбор топлива'):
            browser.element((AppiumBy.XPATH,
                             '//*[@resource-id="ru.tatneft.driver.stage:id/primary" and @text="ДТ ТАНЕКО"]')).click()
        with allure.step('Выбор колонки'):
            browser.element((AppiumBy.XPATH,
                             '//*[@resource-id="ru.tatneft.driver.stage:id/primary" and @text="6"]')).click()
        with allure.step('Ввод объема'):
            browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/editText")).type('3')
            browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/continue_button")).click()
        with allure.step('Проверка итогой страницы заказа'):
            browser.element((AppiumBy.XPATH,
                             '//*[@resource-id="ru.tatneft.driver.stage:id/primary" and @text="ДТ ТАНЕКО"]')).should(be.visible)
            browser.element((AppiumBy.XPATH,
                             '//*[@resource-id="ru.tatneft.driver.stage:id/primary" and @text="3 л"]')).should(
                be.visible)
            browser.element((AppiumBy.XPATH,
                             '//*[@resource-id="ru.tatneft.driver.stage:id/primary" and @text="0728"]')).should(
                be.visible)
            browser.element((AppiumBy.XPATH,
                             '//*[@resource-id="ru.tatneft.driver.stage:id/primary" and @text="6"]')).should(
                be.visible)