import allure
from tests.models.api_requests.requests_report_order import TestReportOrder
from tests.website.api_tests.conftest import swagger_url
from tests.website.data.should_json_schema import should_json


def test_post_order_report(auth):
    report_ops = TestReportOrder(auth, swagger_url)

    with allure.step("Формирование отчета по транзакциям за указанный период"):
        add_response = report_ops.report_order()
        assert add_response.status_code == 200

    with allure.step("Проверка схемы json"):
        should_json(add_response, "post_report.json")
