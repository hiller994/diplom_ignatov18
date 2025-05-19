from tests.models.api_requests.api_base import ApiBase
from tests.website.api_tests.conftest import swagger_url, id_card, id_company, id_driver, id_transport, id_contract
from utils.attach_logging_api import attach_logging
from utils.geterate_date import generate_date

date_from, date_to = generate_date()

class TestReportOrder(ApiBase):
    def report_order(self):
        """Фомирование отчета по транзакциям"""
        endpoint = f'companies/{id_company}/contracts/{id_contract}/reports/'
        payload = {
                                              "format": "PDF",
                                              "date_from": date_from,
                                              "date_to": date_to,
                                              "report_type_id": 2
                                          }

        return self._make_request(
            method="POST",
            endpoint=endpoint,
            json=payload
        )