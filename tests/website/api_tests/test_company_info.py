import json

import allure
import requests
from jsonschema import validate
from tests.website.api_tests.conftest import swagger_url
from utils.attach_logging_api import attach_logging
from utils.file_path import path


def test_get_company_info(auth):
    with allure.step("Отправка запроса"):
        get_company_info = requests.get(url=swagger_url + f'companies/',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth}",
                                               "Content-Type": "application/json"
                                           })
        responce_company_info = get_company_info.json()
        #print(responce_company_info)
    with allure.step("Проверка статус-кода"):
        assert get_company_info.status_code == 200

    with allure.step("Проверка схемы json"):
        schema_path = path("get_company.json")
        with open(schema_path) as file:
            validate(responce_company_info, schema=json.loads(file.read()))

    with allure.step("Сбор логов"):
        attach_logging(get_company_info)
