import subprocess
from pathlib import Path

import pytest
from appium import webdriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene import browser, Config
import os

from path_env import ROOT
from utils.allure_server import post_allure_server_results
from utils.attach_web import attach_screenshot


# Путь к .env.mobile относительно conftest.py
#env_path = Path(__file__).parent.parent.parent.parent / ".env.mobile"
#load_dotenv(env_path)

load_dotenv(os.path.join(ROOT, ".env.mobile")) # Загружаем переменные из .env

#appium_url = os.getenv("MOBILE_URL")
#apk_name = os.getenv("APP")


@pytest.fixture(scope='function')
def mobile_management():
    Config.timeout = 15
    # Получаем абсолютный путь к APK
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apk_path = os.path.abspath(os.path.join(
        current_dir,
        f"../../../tests/mobile/mobile_tests/{os.getenv("APP")}"
    ))

    # Проверяем существование файла
    #if not os.path.exists(apk_path):
    #    pytest.fail(f"APK file not found at: {apk_path}")

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

    #browser.config.driver = webdriver.Remote(
    #    command_executor='http://127.0.0.1:4723',
    #   options=options
    #browser.config.driver_remote_url = os.getenv("MOBILE_URL")
    #browser.config.driver_options = options
    '''
  #ПРИЛОЖЕНИЕ НЕ ЗАКРЫВАЕТСЯ
    browser.config.driver = webdriver.Remote(
        command_executor=os.getenv("MOBILE_URL"),
       options=options
    )

    yield browser
    attach_screenshot(browser)
    post_allure_server_results()

    #browser.terminate_app("ru.****.driver.****")
    # "ru.tatneft.driver.stage" - это package name (идентификатор пакета в Android). Узнать его через adb shell pm list packages.
    # ИНАЧЕ ПРИЛОЖЕНИЕ НЕ ЗАКРЫВАЕТСЯ У МЕНЯ

    browser.quit()



'''
    # Явно создаем драйвер и передаем его Selene
    driver = webdriver.Remote(
        command_executor=os.getenv("MOBILE_URL"),
        options=options
    )
    browser.config.driver = driver

    yield

    attach_screenshot(browser)
    post_allure_server_results()


    #driver.close_app()

    driver.terminate_app(os.getenv("NAME_PACKAGE"))
    #"NAME_PACKAGE" - это package name (идентификатор пакета в Android). Узнать его через adb shell pm list packages.
    # ИНАЧЕ ПРИЛОЖЕНИЕ НЕ ЗАКРЫВАЕТСЯ У МЕНЯ

    driver.quit()
