import json
import os

import pytest
import requests
from jsonschema import validate
from tests.website.conftest import swagger_url
from tests.website.data.file_path import path

web_login = os.getenv("WEB_LOGIN")
web_pass = os.getenv("WEB_PASS")


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
    print(auth_token)
    return auth_token


def test_get_company_info(post_authorization):
    get_company_info = requests.get(url=swagger_url + f'companies/',
                                       headers=
                                       {
                                           "Authorization": f"Bearer {post_authorization}",
                                           "Content-Type": "application/json"
                                       })
    responce_company_info = get_company_info.json()
    print(responce_company_info)

    assert get_company_info.status_code == 200

    schema_path = path("get_company.json")
    with open(schema_path) as file:
        validate(responce_company_info, schema=json.loads(file.read()))
