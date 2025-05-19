from tests.models.api_requests.api_base import ApiBase
from tests.website.api_tests.conftest import swagger_url, id_card, id_company, id_driver, id_transport, id_contract
from utils.attach_logging_api import attach_logging


class TestContractInfo(ApiBase):
    def get_contract_info(self):
        """Получение информации о контракте"""
        endpoint = f'contracts/{id_contract}'

        return self._make_request(
            method="GET",
            endpoint=endpoint
        )