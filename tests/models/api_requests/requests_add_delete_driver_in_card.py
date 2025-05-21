from tests.models.api_requests.api_base import ApiBase
from tests.website.api_tests.conftest import id_card, id_company, id_driver


class TestDriverCardOperations(ApiBase):
    def add_driver_to_card(self):
        """Привязка водителя к топливной карте"""
        endpoint = f'companies/{id_company}/drivers/{id_driver}/cards/'
        payload = {"card_ids": [id_card]}

        return self._make_request(
            method="PATCH",
            endpoint=endpoint,
            json=payload
        )

    def remove_driver_from_card(self):
        """Отвязка водителя от топливной карты"""
        endpoint = f'companies/{id_company}/drivers/{id_driver}/cards/{id_card}/'

        return self._make_request(
            method="DELETE",
            endpoint=endpoint
        )