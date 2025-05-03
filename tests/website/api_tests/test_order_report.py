import json
import os
from datetime import datetime, date, timedelta

import pytest
import requests
from selene import browser
from jsonschema import validate
from conftest import swagger_url
from tests.website.data.file_path import path
from datetime import datetime, timedelta
import random

web_login = os.getenv("WEB_LOGIN")
web_pass = os.getenv("WEB_PASS")
id_contract = os.getenv("ID_CONTRACT")
id_company = os.getenv("ID_COMPANY")

#ГЕНЕРАЦИЯ ДАТЫ
# Текущая дата и дата 6 месяцев назад
end_date = datetime.now()
start_date = end_date - timedelta(days=28 * 6)

# Разница в днях между start_date и end_date
total_days = (end_date - start_date).days

# Генерируем две случайные даты
start = start_date + timedelta(days=random.randint(0, total_days))
end = start + timedelta(days=random.randint(0, (end_date - start).days))

random_start_str = start.strftime('%Y-%m-%d')
random_end_str = end.strftime('%Y-%m-%d')

print(random_start_str)
print(random_end_str)

print(random_start_str)
print(random_end_str)


@pytest.fixture(scope='function')
def post_authorization():
    request_post_authorization = requests.post(url=swagger_url + 'auth/login',
                                               json=
                                               {
                                                   "username": web_login,
                                                   "password": web_pass
                                               })
    responce_post_authorization = request_post_authorization.json()
    #print(responce_post_authorization)
    auth_token = responce_post_authorization['access_token']
    #print(auth_token)
    return auth_token


def test_post_order_report(post_authorization):
    post_order_report = requests.post(url=swagger_url + f'companies/{id_company}/contracts/{id_contract}/reports/',
                                       headers=
                                       {
                                           "Authorization": f"Bearer {post_authorization}",
                                           "Content-Type": "application/json"
                                       },
                                      json=
                                      {
                                          "format": "PDF",
                                          "date_from": random_start_str,
                                          "date_to": random_end_str,
                                          "report_type_id": 2
                                      }
                                      )
    responce_order_report = post_order_report.json()
    print(responce_order_report)

    assert post_order_report.status_code == 200

    schema_path = path("post_report.json")
    with open(schema_path) as file:
        validate(responce_order_report, schema=json.loads(file.read()))