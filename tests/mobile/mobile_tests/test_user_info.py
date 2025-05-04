import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, have


def test_user_info(mobile_management):
    with allure.step('Переход в настройки'):
        #browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/navigation_bar_item_small_label_view")).click()
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/navigation_bar_item_small_label_view" and @text="Настройки"]')).click()
    with allure.step("Открытие формы с информацией о водителе"):
        browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/circle_image_button_image")).click()
    with allure.step("Проверяем ФИО"):
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/value" and @text="Мобилов Автотест Тестович"]')).should(be.visible)
    with allure.step("Проверям номер телефона"):
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/value" and @text="71958040525"]')).should(
            be.visible)