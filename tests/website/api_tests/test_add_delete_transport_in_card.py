import allure
#import requests

from tests.models.api_requests.requests_add_delete_transport_in_card import TestTransportCardOperations
from tests.website.api_tests.conftest import swagger_url, id_card, id_company, id_transport
#from utils.attach_logging_api import attach_logging


def test_delete_driver_card(auth):
    transport_card_ops = TestTransportCardOperations(auth, swagger_url)

    with allure.step("Привязка водителя к топливной карте (перед удалением)"):
        add_response = transport_card_ops.add_transport_to_card()
        assert add_response.status_code == 200

    with allure.step("Отвязка водителя от топливной карты"):
        delete_response = transport_card_ops.remove_transport_from_card()
        assert delete_response.status_code == 200

'''
def test_delete_transport_in_card(auth):
    with allure.step("Привязка транспорта к топливной карте для отвязки"):
        post_add_transport_card = requests.patch(url=swagger_url + f'companies/{id_company}/transports/{id_transport}/cards/{id_card}/',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth}",
                                               "Content-Type": "application/json"
                                           }
                                          )
        responce_add_transport_card = post_add_transport_card.json()
        #print(responce_add_transport_card)

    with allure.step("Проверка статус-кода привязки"):
        assert post_add_transport_card.status_code == 200

    with allure.step("Отвязка транспорта от топливной карты"):
        # потом отвязываем водителя
        post_delete_transport_card = requests.delete(url=swagger_url + f'companies/{id_company}/transports/{id_transport}/cards/{id_card}/',
                                                  headers=
                                                  {
                                                      "Authorization": f"Bearer {auth}",
                                                      "Content-Type": "application/json"
                                                  })
        responce_delete_transport_card = post_delete_transport_card.json()
        #print(responce_delete_transport_card)

    with allure.step("Проверка статус-кода отвязки"):
        assert post_delete_transport_card.status_code == 200

    with allure.step("Сбор логов"):
        attach_logging(post_add_transport_card)
        attach_logging(post_delete_transport_card)
'''