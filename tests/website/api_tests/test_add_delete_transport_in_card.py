import os

import pytest
import requests
from tests.website.conftest import swagger_url

web_login = os.getenv("WEB_LOGIN")
web_pass = os.getenv("WEB_PASS")
id_contract = os.getenv("ID_CONTRACT")
id_company = os.getenv("ID_COMPANY")
id_card = os.getenv("ID_CARD")
id_driver = os.getenv("ID_DRIVER_FOR_CARD")
id_transport = os.getenv("ID_TRANSPORT_FOR_CARD")

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


def test_delete_transport_in_card(post_authorization):
    #сначала привязываем транспорт
    post_add_transport_card = requests.patch(url=swagger_url + f'companies/{id_company}/transports/{id_transport}/cards/{id_card}/',
                                       headers=
                                       {
                                           "Authorization": f"Bearer {post_authorization}",
                                           "Content-Type": "application/json"
                                       }
                                      )
    responce_add_transport_card = post_add_transport_card.json()
    print(responce_add_transport_card)

    assert post_add_transport_card.status_code == 200

    # потом отвязываем водителя
    post_delete_transport_card = requests.delete(url=swagger_url + f'companies/{id_company}/transports/{id_transport}/cards/{id_card}/',
                                              headers=
                                              {
                                                  "Authorization": f"Bearer {post_authorization}",
                                                  "Content-Type": "application/json"
                                              })
    responce_delete_transport_card = post_delete_transport_card.json()
    print(responce_delete_transport_card)

    assert post_delete_transport_card.status_code == 200