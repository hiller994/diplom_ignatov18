import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene import browser, Config
import os

from path_env import ROOT
from utils.allure_server import post_allure_server_results
from utils.attach_web import attach_screenshot

load_dotenv(os.path.join(ROOT, ".env.mobile")) # Загружаем переменные из .env


@pytest.fixture(scope='function')
def mobile_management():
    Config.timeout = 15
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apk_path = os.path.abspath(os.path.join(
        current_dir,
        f"../../../tests/mobile/mobile_tests/{os.getenv("APP")}"
    ))

    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:app": apk_path,
        "appium:allowTestPackages": True,
        "appium:udid": "emulator-5554",
        "appium:ignoreHiddenApiPolicyError": True,
        "appium:enforceAppInstall": False,
        "appium:fullReset": False,
        "appium:noReset": True # Не сбрасывать данные приложения
        #"appium:autoGrantPermission": True
})


    # создаем драйвер и передаем его Selene
    driver = webdriver.Remote(
        command_executor=os.getenv("MOBILE_URL"),
        options=options
    )
    browser.config.driver = driver

    yield

    attach_screenshot(browser)
    post_allure_server_results()

    driver.terminate_app(os.getenv("NAME_PACKAGE"))
    #"NAME_PACKAGE" - это package name (идентификатор пакета в Android). Узнать его через adb shell pm list packages.
    # ИНАЧЕ ПРИЛОЖЕНИЕ НЕ ЗАКРЫВАЕТСЯ У МЕНЯ

    driver.quit()
