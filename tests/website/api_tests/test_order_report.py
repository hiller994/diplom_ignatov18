import json

import allure
import requests
from jsonschema import validate

from tests.models.api_requests.requests_report_order import TestReportOrder
from tests.website.api_tests.conftest import swagger_url, id_company, id_contract
from tests.website.data.should_json_schema import should_json
from utils.file_path import path
from utils.geterate_date import generate_date
from utils.attach_logging_api import attach_logging

def test_post_order_report(auth):
    report_ops = TestReportOrder(auth, swagger_url)

    with allure.step("Формирование отчета по транзакциям за указанный период"):
        add_response = report_ops.report_order()
        assert add_response.status_code == 200

    with allure.step("Проверка схемы json"):
        should_json(add_response, "post_report.json")

        #response_json = add_response.json()
        #schema_path = path("post_report.json")
        #with open(schema_path) as file:
        #    validate(response_json, schema=json.loads(file.read()))
'''
def test_post_order_report(auth):
    with allure.step("Генерация даты для отчета (from - to)"):
        date_from, date_to = generate_date()

    with allure.step("Отправка запроса"):
        post_order_report = requests.post(url=swagger_url + f'companies/{id_company}/contracts/{id_contract}/reports/',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth}",
                                               "Content-Type": "application/json"
                                           },
                                          json=
                                          {
                                              "format": "PDF",
                                              "date_from": date_from,
                                              "date_to": date_to,
                                              "report_type_id": 2
                                          }
                                          )
        responce_order_report = post_order_report.json()
        #print(responce_order_report)

    with allure.step("Проверка статус-кода"):
        assert post_order_report.status_code == 200

    with allure.step("Проверка схемы json"):
        schema_path = path("post_report.json")
        with open(schema_path) as file:
            validate(responce_order_report, schema=json.loads(file.read()))

    with allure.step('Сбор логов'):
        attach_logging(post_order_report)
'''
