import time

import allure
import requests
from selene import browser, have

from tests.website.ui_tests.conftest import swagger_url, id_contract

class AddcardgroupPage:
    #Сделал id_group и auth_data атрибутами класса, чтобы они были доступны во всех методах
    def __init__(self):
        self.id_group = None
        self.auth_data = None

    @allure.step('Создание группы')
    def create_group(self):
        self.auth_data = browser.execute_script('''
                                return {
                                    auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                    user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                                };
                            ''')
        create_card_group = requests.post(url=swagger_url + f'contracts/{id_contract}/card-groups/', headers=
        {
            "Authorization": f"Bearer {self.auth_data['auth']['accessToken']}",
            "Content-Type": "application/json"
        },
                                          json={
                                              "name": "Тестовая группа селен12",
                                              "comment": "Создание группы через автотест1"
                                          })

        data_card_group = create_card_group.json()
        self.id_group = data_card_group['id']
        return self.auth_data, self.id_group

    @allure.step('Открытие формы создания лимита')
    def open_page(self):
        browser.open(f'groups/{self.id_group}')
        browser.element('[class="btn btn--fit btn--green"]').click()

    @allure.step('Выбор карты для добавления')
    def add_card_in_group(self, value_number_card):
        browser.element('[placeholder="Поиск по номеру карты"]').type(value_number_card)
        time.sleep(1)
        browser.element('[class="flex checkbox"]').click() #выбрали карту
        browser.element('[class="btn btn--green"]').click() #клик добавить
        time.sleep(0.5)

    @allure.step('Сохранение добавленной карты, возврат в гурппу')
    def save_card_in_group(self):
        browser.element('[class="btn btn--green"]').click() #клик продолжить (инфа о переносе)
        time.sleep(0.5)
        browser.element('[class="btn btn--green"]').click() #вернуться к группе
        time.sleep(0.5)

    @allure.step('Проверка отображения карты в списке')
    def should_card_in_group(self, value_number_card):
        browser.element('[class="card-number"]').should(have.text(value_number_card))
        #time.sleep(2)

    @allure.step('Удаление группы')
    def delete_group(self):
        delete_group = requests.delete(url=swagger_url + f'contracts/{id_contract}/card-groups/{self.id_group}',
                                      headers=
                                      {
                                          "Authorization": f"Bearer {self.auth_data['auth']['accessToken']}",
                                          "Content-Type": "application/json"
                                      })
        data_delete_group = delete_group.json()
        print(data_delete_group)

