import os

import allure
import requests
from selene import browser, have

from tests.website.ui_tests.conftest import swagger_url


class UserinfoPage:
    def __init__(self):
        self.company_name = None
        #self.company_address = None

    @allure.step('Открытие настроек личного кабинета')
    def open_page(self):
        browser.open("settings")

    @allure.step('Запрос информации по учетке (api)')
    def request_userinfo(self):
            auth_data = browser.execute_script('''
                                        return {
                                            auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                            user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                                        };
                                    ''')
            # запрос
            requests_userinfo = requests.get(
                url=swagger_url + f'auth/userinfo', headers=
                {
                    "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                    "Content-Type": "application/json"
                })
            data_userinfo = requests_userinfo.json()

            #Доступ к элементам списка осуществляется по индексу, а не по ключу
            self.company_name = data_userinfo['contracts'][0]['company']['name']
            #company_address = data_userinfo['contracts'][0]['company']['address']
            return self.company_name

    @allure.step('Сравнение данных фронта и ответа с бэка')
    def should_data(self):
        browser.element('.card__block').should(have.text(self.company_name)) #проверить, что текст просто содержится где-то внутри блока
        #browser.element('.card__block').should(have.text(company_address))