import allure
from tests.models.api_requests.requests_contract_info import TestContractInfo
from tests.website.api_tests.conftest import swagger_url
from tests.website.data.should_json_schema import should_json


def test_get_contract_info(auth):
    contract_ops = TestContractInfo(auth, swagger_url)

    with allure.step("Запрос информации о договоре"):
        add_response = contract_ops.get_contract_info()
        assert add_response.status_code == 200

    with allure.step('Проверка схемы json'):
        should_json(add_response, "get_contract.json")