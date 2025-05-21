from tests.models.api_requests.api_base import ApiBase


class TestCompanyInfo(ApiBase):
    def get_company_info(self):
        """Получение информации о компании"""
        endpoint = 'companies/'

        return self._make_request(
            method="GET",
            endpoint=endpoint
        )