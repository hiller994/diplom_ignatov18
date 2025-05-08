import allure
import requests
from selene import browser, have, be

from tests.website.conftest import swagger_url


def test_auth(auth):
    with allure.step("Проверка авторизации"):
        browser.open("settings")

    with allure.step("Отправляем запрос по компании"):
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
        company_name = data_userinfo['contracts'][0]['company']['name']
        #company_address = data_userinfo['contracts'][0]['company']['address']

    with allure.step('Сравниваем значения адреса и компании на вэбе с ответом бэка'):
        browser.element('.card__block').should(have.text(company_name)) #проверить, что текст просто содержится где-то внутри блока
        #browser.element('.card__block').should(have.text(company_address))