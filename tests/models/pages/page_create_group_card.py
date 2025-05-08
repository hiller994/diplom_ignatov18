import allure
import requests
from selene import browser, have, be

from tests.website.conftest import swagger_url, id_contract


class GroupcardPage:
    @allure.step('Открытие формы создания группы карт')
    def open_page(self):
        browser.open('cards?tab=2')
        browser.element('[class="btn btn--fit btn--green"]').click()

    @allure.step('Ввод названия группы и примечания')
    def type_name_group_and_note(self, value_name, value_note):
        browser.element('[placeholder="Введите название"]').type(value_name) #Тестовая группа селен
        browser.element('[placeholder="Введите примечание"]').type(value_note) #Тестовое описание группы, созданное через автотест

    @allure.step('Сохранение группы')
    def save_group(self):
        browser.element('[class="btn btn--green"]').click()  # сохранение
        #browser.element('[class="green"]').should(have.text('Тестовая группа селен'))
        browser.element('[class="btn btn--green"]').click()  # открытие созданной группы

    @allure.step('Проверка открытие страници группы')
    def should_save_group(self, value_note):
        browser.element(f'//*[contains(text(), "{value_note}")]').should(
            be.visible) #Тестовое описание группы, созданное через автотест

    @allure.step('Удаление группы (api)')
    def delete_group(self, value_name):

        auth_data = browser.execute_script('''
                            return {
                                auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                            };
                        ''')
        # запрос на группы карт
        requests_groups_card = requests.get(
            url=swagger_url + f'contracts/{id_contract}/card-groups/?page=1&size=20&contract_id={id_contract}', headers=
            {
                "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                "Content-Type": "application/json"
            })
        data_groups_card = requests_groups_card.json()

        # Проверяем наличие ключа 'items' в ответе
        target_name_group = value_name #'Тестовая группа селен'
        group_id = None

        if 'items' in data_groups_card:
            # Перебираем всех пользователей
            for user in data_groups_card['items']:
                # Проверяем совпадение названия группы (с учетом регистра)
                if user.get('name') == target_name_group:
                    group_id = user['id']
                    break
        # удаление группы
        delete_oper = requests.delete(url=swagger_url + f'contracts/{id_contract}/card-groups/?group_ids={group_id}',
                                      headers=
                                      {
                                          "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                          "Content-Type": "application/json"
                                      })
        responce_delete_group_card = delete_oper.json()
        print(responce_delete_group_card)


