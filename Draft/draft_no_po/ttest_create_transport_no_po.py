import time

import allure
import requests
from selene import browser, have

from tests.website.ui_tests.conftest import swagger_url, id_company


def test_create_driver(auth):
    with allure.step("Cоздания транспорта"):
        browser.open("transports")
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Введите марку"]').type("Автотест-марка")
        browser.element('[placeholder="Введите модель"]').type("Автотест-модель")
        browser.element('[class="select"]').click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "Россия")]').click()
        #browser.element('[class="input-wrapper"]').click()
        time.sleep(1)
        #browser.element('[class="input-wrapper"]').type('М658716')
        #browser.element('[placeholder=""]').type('М658716')
        browser.element('//*[@id="app"]/div/main/div[4]/div[2]/div/div[1]/div[4]/div[2]/input').type('М719ММ716')
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="table__content__item"]').should(have.text('Автотест-марка'))
        browser.element('//*[contains(@class, "number") and contains(text(), "М719ММ716")]').click()
    with allure.step("Получение списка транспорта (для удаления)"):
        # достаем данные из localStorage
        auth_data = browser.execute_script('''
                                    return {
                                        auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                        user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                                    };
                                ''')
        # отправляем запрос на получение транспорта
        requests_transports = requests.get(
            url=swagger_url + f'companies/{id_company}/transports/?page=1&size=10&sort=-updated_at', headers=
            {
                "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                "Content-Type": "application/json"
            })
        data_transports = requests_transports.json()

        # Ищем транспорт по номеру
        target_number = "М719ММ716"  # Номер транспорта, которое ищем
        ts_id = None

        # Проверяем наличие ключа 'items' в ответе
        if 'items' in data_transports:
            # Перебираем всех водителей
            for user in data_transports['items']:
                # Проверяем совпадение номера (с учетом регистра)
                if user.get('reg_number') == target_number:
                    ts_id = user['id']
                    break

        with allure.step("Удаление транспорта"):
            # Удаление транспорта
            delete_transport = requests.delete(url=swagger_url + f'companies/{id_company}/transports/?transport_id={ts_id}',
                                            headers=
                                            {
                                                "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                                "Content-Type": "application/json"
                                            })
            responce_delete_transport = delete_transport.json()
            print(responce_delete_transport)
            

