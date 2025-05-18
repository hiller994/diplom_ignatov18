import requests

from tests.models.api_requests.api_base import ApiBase
from tests.website.api_tests.conftest import swagger_url, id_card, id_company, id_driver, id_transport
from utils.attach_logging_api import attach_logging


class TestTransportCardOperations(ApiBase):
    def add_transport_to_card(self):
        """Привязка транспорта к топливной карте для отвязки"""
        endpoint = f'{self.base_url}companies/{id_company}/transports/{id_transport}/cards/{id_card}/'

        return self._make_request(
            method="PATCH",
            endpoint=endpoint
        )

    def remove_transport_from_card(self):
        """Отвязка транспорта от топливной карты"""
        endpoint = f'{self.base_url}companies/{id_company}/transports/{id_transport}/cards/{id_card}/'

        return self._make_request(
            method="DELETE",
            endpoint=endpoint
        )