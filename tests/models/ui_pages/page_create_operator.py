import allure
import requests
from selene import browser, have

from tests.website.ui_tests.conftest import swagger_url, id_company


class OperatorPage:
    @allure.step('Открытие формы создания оператора')
    def open_page(self):
        browser.open("drivers?tab=1")
        browser.element('[class="btn btn--fit btn--green"]').click()

    @allure.step('Ввод ФИО')
    def type_fio(self, value_family_name, value_first_name, value_middle_name):
        browser.element('[placeholder="Введите фамилию"]').type(value_family_name)
        browser.element('[placeholder = "Введите имя"]').type(value_first_name)
        browser.element('[placeholder="Введите отчество"]').type(value_middle_name)
        return value_family_name, value_first_name, value_middle_name

    @allure.step('Ввод номера телефона')
    def type_number(self, value_number):
        browser.element('[placeholder = "Введите номер телефона"]').type(value_number)

    @allure.step('Ввод электронной почты')
    def type_email(self, value_email):
        browser.element('[placeholder="Введите адрес электронной почты"]').type(value_email)
        return value_email

    @allure.step('Ввод примечания')
    def type_note(self, value_note):
        browser.element('[placeholder="Введите примечание"]').type(value_note)

    @allure.step('Выбор договора')
    def add_contract(self, value_contract):
        browser.element('[class ="btn btn--green"]').click()
        browser.element(
            f'//div[contains(@class, "item__flex") and contains(., "{value_contract}")]//*[contains(@class, "flex checkbox")]').click()

    @allure.step('Сохранение оператора и возврат к списку')
    def save_opetator(self):
        browser.element('[class="btn btn--green"]').click()  # клик 'Сохранить'
        browser.element('[class="btn btn--green"]').click()  # клик 'Вернуться к списку'

    @allure.step('Проверка появления операто в списке')
    def should_save_operator(self, value_family_name, value_email):
        browser.element('[class="table__item"]').should(have.text(value_family_name))
        browser.element(f'//*[contains(@class, "mail") and contains(text(), "{value_email}")]').click()
        browser.element('[class="operator"]').should(have.text('Данные оператора'))

    @allure.step('Удаление оператора (api)')
    def delete_operator(self, value_fio):
        auth_data = browser.execute_script('''
                    return {
                        auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                        user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                    };
                ''')


        requests_users = requests.get(url=swagger_url + f'companies/{id_company}/users/?page=1&size=10&sort=-updated_at', headers =
    {
    "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
    "Content-Type": "application/json"
    })
        data_users = requests_users.json()

        #print(data_users)

        # 3. Ищем пользователя по ФИО
        target_fio = value_fio  # ФИО, которое ищем
        user_id = None

        # Проверяем наличие ключа 'items' в ответе
        if 'items' in data_users:
            # Перебираем всех пользователей
            for user in data_users['items']:
                # Проверяем совпадение ФИО (с учетом регистра)
                if user.get('fio') == target_fio:
                    user_id = user['id']
                    break


        delete_oper = requests.delete(url=swagger_url + f'companies/{id_company}/users/?user_id={user_id}',
                                      headers=
                                      {
                                          "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                          "Content-Type": "application/json"
                                      })
        responce_delete_oper = delete_oper.json()
        print(responce_delete_oper)