import allure
import requests
from selene import browser, have

from tests.website.conftest import swagger_url, id_company

class DriverPage:
    @allure.step('Открытие формы создания водителя')
    def open_page(self):
        browser.open("drivers?tab=0")
        browser.element('[class="btn btn--fit btn--green"]').click()

    @allure.step('Ввод ФИО')
    def type_fio(self, valuer_family_name, valuer_first_name, valuer_last_name):
        browser.element('[placeholder="Введите фамилию"]').type(valuer_family_name)
        browser.element('[placeholder = "Введите имя"]').type(valuer_first_name)
        browser.element('[placeholder="Введите отчество"]').type(valuer_last_name)

    @allure.step('Ввод номера телефона')
    def type_number(self, value_number):
        browser.element('[placeholder = "Введите номер телефона"]').type(value_number)

    @allure.step('Ввод примечания')
    def type_note(self, value_note):
        browser.element('[placeholder="Введите примечание"]').type(value_note)
        browser.element('[class ="btn btn--green"]').click()  # клик 'Сохранить'

    @allure.step('Прикрепление карты к водителю')
    def add_card(self, value_card_number):
        browser.element('[placeholder="Поиск по номеру"]').type(value_card_number) #7013420000010876
        browser.element(f'//*[contains(text(), "{value_card_number}")]').click()

    @allure.step('Сохранение водителя и возврат к списку')
    def save_driver(self):
        browser.element('[class="btn btn--green"]').click()  # клик 'Сохранить'
        browser.element('[class="btn btn--green"]').click()  # клик 'Вернуться к списку'

    @allure.step('Проверка появления водителя в списке')
    def should_save_driver(self, valuer_family_name, value_number):
        browser.element('[class="table__item"]').should(have.text(valuer_family_name))
        browser.element(f'//*[contains(@class, "phone") and contains(text(), "{value_number}")]').click()
        browser.element('[class="driver"]').should(have.text('Данные водителя'))

    @allure.step('Удаление водителя')
    def delete_driver(self, value_fio):
        # достаем данные из localStorage
        auth_data = browser.execute_script('''
                            return {
                                auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                            };
                        ''')
        # отправляем запрос на получение водителей
        requests_drivers = requests.get(
            url=swagger_url + f'companies/{id_company}/drivers/?page=1&size=10&sort=-updated_at', headers=
            {
                "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                "Content-Type": "application/json"
            })
        data_drivers = requests_drivers.json()

        # Ищем пользователя по ФИО
        target_fio = value_fio  # ФИО, которое ищем
        driver_id = None

        # Проверяем наличие ключа 'items' в ответе
        if 'items' in data_drivers:
            # Перебираем всех водителей
            for user in data_drivers['items']:
                # Проверяем совпадение ФИО (с учетом регистра)
                if user.get('fio') == target_fio:
                    driver_id = user['id']
                    break

        #Удаление водителя
        delete_driver = requests.delete(url=swagger_url + f'companies/{id_company}/drivers/?driver_id={driver_id}',
                                      headers=
                                      {
                                          "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                          "Content-Type": "application/json"
                                      })
        responce_delete_drive = delete_driver.json()
        print(responce_delete_drive)
