"""
- АВТОРИЗАЦИЯ API
- ШАГИ СОЗДАНИЯ И СОХРАЕНИЯ API
- ПРОВЕРКА WEB
- УДАЛЕНИЕ API
"""

import allure
import requests
from selene import browser, have

from tests.website.conftest import swagger_url, id_company


def test_create_driver():
    with allure.step("создание оператора (api)"):

        auth_data = browser.execute_script('''
            return {
                auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
            };
        ''')

        create_oper = requests.post(url=swagger_url + f'companies/{id_company}/users/', headers =
    {
    "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
    "Content-Type": "application/json"
    },
                                     json={
                                            "phone_number": "70000000001",
                                            "family_name": "Селенов",
                                            "given_name": "Оператор",
                                            "middle_name": "Тестович",
                                            "email": "selene_po4ta_for_test@gmail.com",
                                            "comment": "Создание оператора через автотест (создание - апи, проверка - веб)"
                                     })

        data_oper = create_oper.json()
        print(data_oper)
        print(auth_data['user']['id'])
        print(auth_data['user'])

    with allure.step("Проврека создания оператора"):
        browser.open('drivers?tab=1')
        browser.element('//*[contains(@class, "mail") and contains(text(), "selene_po4ta_for_test@gmail.com")]').click()
        browser.element('[class="flex flex--space-between"]').should(have.text('Данные оператора'))


    with allure.step('Удаление оператора'):
        delete_oper = requests.delete(url=swagger_url + f'companies/{id_company}/users/?user_id={data_oper['id']}', headers =
    {
    "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
    "Content-Type": "application/json"
    })
        responce_delete_oper = delete_oper.json()
        print(responce_delete_oper)
        #browser.element('[placeholder="Введите фамилию"]').should(be.blank)
        #browser.open('cards/836b67b5-248e-41d0-b4b9-a0cc5dc85271?tab=1')
        #time.sleep(3)
        #browser.element('')