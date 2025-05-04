import json

import allure
import pytest
import requests
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach
from dotenv import load_dotenv
import os
load_dotenv() # Загружаем переменные из .env помогло

DEFAULT_BROWSER_VERSION = "128.0"

web_login = os.getenv("WEB_LOGIN")
web_pass = os.getenv("WEB_PASS")
web_url = os.getenv("WEB_URL")
swagger_url = os.getenv("SWAGGER_URL")
id_company = os.getenv("ID_COMPANY")
id_card = os.getenv("ID_CARD")
id_contract = os.getenv("ID_CONTRACT")

def pytest_addoption(parser):
    parser.addoption("--browser_version", default="128.0")




@pytest.fixture(scope='function')
def auth():
    with allure.step("Получение токена"):
        result_token = requests.post(url=swagger_url + 'auth/login',
                               json={
                                   "password" : web_pass,
                                   "username" : web_login
                               })
        data_token = result_token.json()
        #print(data_token)
    with allure.step("Запрос информации лк по токену"):
        result_userinfo = requests.get(url=swagger_url + 'auth/userinfo', headers={'Authorization': f'bearer ' + data_token['access_token']})
        data_userinfo = result_userinfo.json()


    with allure.step("Сохранение данных авторизации в local_storage"):
        browser.open(web_url)
        def snake_to_camel(s):
            words = s.split('_') #Разбивает исходную строку по символу '_' на список слов.
            return words[0] + ''.join(word.capitalize() for word in words[1:])
            #(word.capitalize() for word in ...) - Каждое слово из списка преобразуется с помощью capitalize(), который делает первую букву заглавной, а остальные — строчными.
            #''.join(...) Объединяет все слова из генератора в одну строку без разделителей.
            #[0] Если первое слово должно быть с маленькой буквы (как в camelCase),

        camel_case_login = {
            snake_to_camel(key): value
            for key, value in data_token.items()
            if key in ["access_token", "expires_at", "refresh_token", "token_type"]
        }
        camel_case_userinfo = {
            snake_to_camel(key): value
            for key, value in data_userinfo.items()
            if key in ["email", "email_verified", "family_name", "given_name", "id", "is_registering", "phone_number",
                       "phone_number_verified", "updated_at"]
        }

        local_storage_information = browser.execute_script(f'''
                             localStorage.setItem(".tn_gsb.tn_auth", JSON.stringify({camel_case_login}));
                             localStorage.setItem(".tn_gsb.tn_user", JSON.stringify({json.dumps(camel_case_userinfo)}));
                            window.dispatchEvent(new Event('storage'));
                         ''')

        browser.open(web_url)  # обновляем страницу




@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption("--browser_version")
    browser_version = (
        browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    )
    browser.config.base_url = web_url

    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = "eager"
    browser.config.driver_options = driver_options
    browser.config.window_width = 1920
    browser.config.window_height = 1080


    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {"enableVNC": True, "enableVideo": True},
    }

    options.capabilities.update(selenoid_capabilities)
    #browser.config.driver = webdriver.Remote(
    #    command_executor=f"https://{selenoid_login}:{selenoid_pass}@selenoid.autotests.cloud/wd/hub",
    #    options=options,
    #)

    yield
    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    #attach.add_video(browser)
    browser.quit()