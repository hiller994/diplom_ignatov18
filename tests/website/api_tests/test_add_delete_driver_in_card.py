import allure
#import requests

from tests.models.api_requests.requests_add_delete_driver_in_card import TestDriverCardOperations
from tests.website.api_tests.conftest import swagger_url


#from tests.website.api_tests.conftest import swagger_url, id_card, id_company, id_driver
#from utils.attach_logging_api import attach_logging


def test_delete_driver_card(auth):
    driver_card_ops = TestDriverCardOperations(auth, swagger_url)

    with allure.step("Привязка водителя к топливной карте (перед удалением)"):
        add_response = driver_card_ops.add_driver_to_card()
        assert add_response.status_code == 200

    with allure.step("Отвязка водителя от топливной карты"):
        delete_response = driver_card_ops.remove_driver_from_card()
        assert delete_response.status_code == 200



'''
def test_delete_driver_card(auth):
    #сначала привязываем водителя
    with allure.step("Привязка водителя к топливной карте (перед удалением)"):
        post_add_driver_card = requests.patch(url=swagger_url + f'companies/{id_company}/drivers/{id_driver}/cards/',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth}",
                                               "Content-Type": "application/json"
                                           },
                                          json=
                                             {
                                                 "card_ids": [
                                                     id_card
                                                 ]
                                             }
                                          )
        responce_add_driver_card = post_add_driver_card.json()

        with allure.step('Проверка статус-кода привязки'):
            assert post_add_driver_card.status_code == 200

    with allure.step("Отвязка водителя от топливной карты"):
        # потом отвязываем водителя
        post_delete_driver_card = requests.delete(url=swagger_url + f'companies/{id_company}/drivers/{id_driver}/cards/{id_card}/',
                                                  headers=
                                                  {
                                                      "Authorization": f"Bearer {auth}",
                                                      "Content-Type": "application/json"
                                                  })
        responce_delete_driver_card = post_delete_driver_card.json()

        with allure.step('Проверка статус-кода отвязки'):
            assert post_delete_driver_card.status_code == 200

    with allure.step("Сбор логов"):
        attach_logging(post_add_driver_card)
        attach_logging(post_delete_driver_card)
'''