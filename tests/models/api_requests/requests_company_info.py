import requests

from tests.models.api_requests.api_base import ApiBase
from tests.website.api_tests.conftest import swagger_url, id_card, id_company, id_driver, id_transport
from utils.attach_logging_api import attach_logging


class TestCompanyInfo(ApiBase):
    def get_company_info(self):
        """Получение информации о компании"""
        endpoint = 'companies/'

        return self._make_request(
            method="GET",
            endpoint=endpoint
        )