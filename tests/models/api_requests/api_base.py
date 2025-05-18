import requests
from utils.attach_logging_api import attach_logging

#Вынес общую логику в базовый класс и затем наследуюсь от него в других тестах апи
class ApiBase:
    def __init__(self, auth_token, base_url):
        self.auth_token = auth_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method, endpoint, **kwargs):
        """Общий метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            **kwargs
        )
        attach_logging(response)
        return response