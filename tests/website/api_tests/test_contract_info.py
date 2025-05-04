import json
import os

import pytest
import requests
from jsonschema import validate
from tests.website.conftest import swagger_url
from tests.website.data.file_path import path

web_login = os.getenv("WEB_LOGIN")
web_pass = os.getenv("WEB_PASS")
id_contract = os.getenv("ID_CONTRACT")

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


def test_get_contract_info(post_authorization):
    get_contract_info = requests.get(url=swagger_url + f'contracts/{id_contract}',
                                       headers=
                                       {
                                           "Authorization": f"Bearer {post_authorization}",
                                           "Content-Type": "application/json"
                                       })
    responce_contract_info = get_contract_info.json()
    print(responce_contract_info)

    assert get_contract_info.status_code == 200

    schema_path = path("get_contract.json")
    with open(schema_path) as file:
        validate(responce_contract_info, schema=json.loads(file.read()))