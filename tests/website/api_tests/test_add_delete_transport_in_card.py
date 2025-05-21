import allure
from tests.models.api_requests.requests_add_delete_transport_in_card import TestTransportCardOperations
from tests.website.api_tests.conftest import swagger_url


def test_delete_driver_card(auth):
    transport_card_ops = TestTransportCardOperations(auth, swagger_url)

    with allure.step("Привязка водителя к топливной карте (перед удалением)"):
        add_response = transport_card_ops.add_transport_to_card()
        assert add_response.status_code == 200

    with allure.step("Отвязка водителя от топливной карты"):
        delete_response = transport_card_ops.remove_transport_from_card()
        assert delete_response.status_code == 200