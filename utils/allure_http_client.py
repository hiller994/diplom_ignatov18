import os

import requests
from dotenv import load_dotenv

from path_env import ROOT

load_dotenv(os.path.join(ROOT, ".env.allure_server"))

allure_login = os.getenv('ALLURE_LOGIN')
allure_pass = os.getenv('ALLURE_PASS')
allure_url_web = os.getenv('ALLURE_URL_WEB')
allure_url_swagger = os.getenv('ALLURE_URL_SWAGGER')
id_project = os.getenv('ALLURE_ID_PROJECT')

from utils.attach_logging_api import attach_logging

#Вынес общую логику в базовый класс и затем наследуюсь от него в других тестах апи
class AllureClient:
    def __init__(self, headers=None):
        self.base_url = allure_url_swagger
        self.headers = headers or {}
        self.json = {
            "username": os.getenv('ALLURE_LOGIN'),
            "password": os.getenv('ALLURE_PASS')
        }
        self.session = requests.Session()

    def allure_request(self, method, endpoint, **kwargs):
        """Общий метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(  # Используем self.session вместо requests
            method=method,
            url=url,
            headers=self.headers,
            **kwargs
        )
        return response