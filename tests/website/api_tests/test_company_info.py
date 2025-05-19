#import json
import json

import allure
#import requests
from jsonschema import validate

from tests.models.api_requests.requests_company_info import TestCompanyInfo
from tests.website.data.should_json_schema import should_json
from tests.website.ui_tests.conftest import swagger_url
from utils.file_path import path


#from tests.website.api_tests.conftest import swagger_url
#from utils.attach_logging_api import attach_logging
#from utils.file_path import path

def test_delete_driver_card(auth):
    company_ops = TestCompanyInfo(auth, swagger_url)

    with allure.step("Запрос информации о компании"):
        add_response = company_ops.get_company_info()
        assert add_response.status_code == 200

    with allure.step("Проверка схемы json"):
        should_json(add_response, "get_company.json")
        #response_json = add_response.json()
        #schema_path = path("get_company.json")
        #with open(schema_path) as file:
        #    validate(response_json, schema=json.loads(file.read()))

'''
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
'''