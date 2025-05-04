import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, have


def test_user_info(mobile_management):
    with allure.step('Переход в раздел с картами'):
        #browser.element((AppiumBy.ID, "ru.tatneft.driver.stage:id/navigation_bar_item_small_label_view")).click()
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/navigation_bar_item_small_label_view" and @text="Мои карты"]')).click()
    with allure.step("Переход на страницу с информацией о карте"):
        browser.element((AppiumBy.XPATH,
                         '//*[@resource-id="ru.tatneft.driver.stage:id/card_number" and @text="0728"]')).click()
    with allure.step("Отображение на странице информации по карте"):
        browser.element((AppiumBy.XPATH,
                         '//*[@class="android.widget.TextView" and @text="Лимиты по карте"]')).should(be.visible)