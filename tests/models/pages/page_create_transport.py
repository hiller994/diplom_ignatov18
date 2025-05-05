import allure
import requests
from selene import browser, have

from tests.website.conftest import swagger_url, id_company

class TransportPage:
    @allure.step('Открытие формы создания транспорта')
    def open_page(self):
        browser.open("transports")
        browser.element('[class="btn btn--fit btn--green"]').click()

    @allure.step('Ввод Марки и Модели')
    def type_brand_and_model(self, value_brand, valuer_model):
        browser.element('[placeholder="Введите марку"]').type(value_brand)
        browser.element('[placeholder="Введите модель"]').type(valuer_model)

    @allure.step('Выбор страны')
    def select_country(self, value_country):
            browser.element('[class="select"]').click()
            browser.element(f'//*[contains(@class, "select__option") and contains(text(), "{value_country}")]').click()

    @allure.step('Ввод номера транспорта согласно стране')
    def type_number(self, value_number):
        browser.element('//*[@id="app"]/div/main/div[4]/div[2]/div/div[1]/div[4]/div[2]/input').type(value_number)

    @allure.step('Сохранение транспорта и возврат к списку')
    def save_transport(self):
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="btn btn--green"]').click()

    @allure.step('Проверка появления транспорта в списке')
    def should_save_transport(self, value_brand, value_number):
        browser.element('[class="table__content__item"]').should(have.text(value_brand))
        browser.element(f'//*[contains(@class, "number") and contains(text(), "{value_number}")]').click()

    @allure.step('Удаление авто')
    def delete_transport(self, value_number):
        #Получение списка транспорта (для удаления)
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
        target_number = value_number  # Номер транспорта, которое ищем
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
            delete_transport = requests.delete(
                url=swagger_url + f'companies/{id_company}/transports/?transport_id={ts_id}',
                headers=
                {
                    "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                    "Content-Type": "application/json"
                })
            responce_delete_transport = delete_transport.json()
            print(responce_delete_transport)


