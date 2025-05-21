import allure

from tests.models.api_requests.requests_add_delete_driver_in_card import TestDriverCardOperations
from tests.website.api_tests.conftest import swagger_url


def test_delete_driver_card(auth):
    driver_card_ops = TestDriverCardOperations(auth, swagger_url)

    with allure.step("Привязка водителя к топливной карте (перед удалением)"):
        add_response = driver_card_ops.add_driver_to_card()
        assert add_response.status_code == 200

    with allure.step("Отвязка водителя от топливной карты"):
        delete_response = driver_card_ops.remove_driver_from_card()
        assert delete_response.status_code == 200