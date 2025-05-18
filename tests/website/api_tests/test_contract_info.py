import json

import allure
import requests
from jsonschema import validate

from tests.models.api_requests.requests_contract_info import TestContractInfo
from tests.website.api_tests.conftest import swagger_url, id_contract
from utils.attach_logging_api import attach_logging
from utils.file_path import path

def test_get_contract_info(auth):
    contract_ops = TestContractInfo(auth, swagger_url)

    with allure.step("Запрос информации о договоре"):
        add_response = contract_ops.get_contract_info()
        assert add_response.status_code == 200

    with allure.step('Проверка схемы json'):
        schema_path = path("get_contract.json")
        with open(schema_path) as file:
            validate(add_response, schema=json.loads(file.read()))
'''
def test_get_contract_info(auth):
    with allure.step('Отправка запроса'):
        get_contract_info = requests.get(url=swagger_url + f'contracts/{id_contract}',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth}",
                                               "Content-Type": "application/json"
                                           })
        responce_contract_info = get_contract_info.json()
        #print(responce_contract_info)

    with allure.step('Проверка статус-кода'):
        assert get_contract_info.status_code == 200

    with allure.step('Проверка схемы json'):
        schema_path = path("get_contract.json")
        with open(schema_path) as file:
            validate(responce_contract_info, schema=json.loads(file.read()))

    with allure.step('Сбор логов'):
        attach_logging(get_contract_info)
'''