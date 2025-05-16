import allure
import pytest
import requests
from selene.support.shared import browser
from dotenv import load_dotenv
import os

from tests.website.ui_tests.allure_server import post_allure_server_results

load_dotenv()

web_login = os.getenv("WEB_LOGIN")
web_pass = os.getenv("WEB_PASS")
web_url = os.getenv("WEB_URL")
swagger_url = os.getenv("SWAGGER_URL")
id_company = os.getenv("ID_COMPANY")
id_card = os.getenv("ID_CARD")
id_contract = os.getenv("ID_CONTRACT")
id_driver = os.getenv("ID_DRIVER_FOR_CARD")
id_transport = os.getenv("ID_TRANSPORT_FOR_CARD")


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
        token = data_token['access_token']

    yield token

    post_allure_server_results()  # отправка отчета на сервер