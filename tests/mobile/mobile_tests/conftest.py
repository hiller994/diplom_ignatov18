import pytest
from appium.options.android import UiAutomator2Options
from selene import browser, Config
import os

from utils.attach import attach_screenshot



@pytest.fixture(scope='function')
def mobile_management():
    Config.timeout = 15
    # Получаем абсолютный путь к APK
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apk_path = os.path.abspath(os.path.join(
        current_dir,
        "../../../tests/mobile/mobile_tests/***.apk"
    ))

    # Проверяем существование файла
    if not os.path.exists(apk_path):
        pytest.fail(f"APK file not found at: {apk_path}")

    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:app": apk_path,
        "appium:allowTestPackages": True,
        "appium:udid": "emulator-5554",
        "appium:ignoreHiddenApiPolicyError": True,
        "appium:enforceAppInstall": False,
        #"appium:noReset": True
        "appium:fullReset": False,
        "noReset": True # Не сбрасывать данные приложения
})

    #browser.config.driver = webdriver.Remote(
    #    command_executor='http://127.0.0.1:4723',
    #   options=options
    browser.config.driver_remote_url = "http://127.0.0.1:4723"
    browser.config.driver_options = options



    yield

    attach_screenshot(browser)
    browser.quit()