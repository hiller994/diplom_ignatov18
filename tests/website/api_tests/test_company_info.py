import allure
from tests.models.api_requests.requests_company_info import TestCompanyInfo
from tests.website.data.should_json_schema import should_json
from tests.website.ui_tests.conftest import swagger_url


def test_delete_driver_card(auth):
    company_ops = TestCompanyInfo(auth, swagger_url)

    with allure.step("Запрос информации о компании"):
        add_response = company_ops.get_company_info()
        assert add_response.status_code == 200

    with allure.step("Проверка схемы json"):
        should_json(add_response, "get_company.json")