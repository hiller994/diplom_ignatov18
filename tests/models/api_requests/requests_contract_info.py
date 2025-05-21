from tests.models.api_requests.api_base import ApiBase
from tests.website.api_tests.conftest import id_contract

class TestContractInfo(ApiBase):
    def get_contract_info(self):
        """Получение информации о контракте"""
        endpoint = f'contracts/{id_contract}'

        return self._make_request(
            method="GET",
            endpoint=endpoint
        )