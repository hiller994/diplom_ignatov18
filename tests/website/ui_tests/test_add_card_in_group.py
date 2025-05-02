import time

import allure
import requests
from selene import browser, have, be

from conftest import swagger_url, id_contract


def test_add_card_in_group():
    with allure.step("Создание группы (для добавление карты)"):
        auth_data = browser.execute_script('''
                                    return {
                                        auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                        user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                                    };
                                ''')
        create_card_group = requests.post(url=swagger_url + f'contracts/{id_contract}/card-groups/', headers=
        {
            "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
            "Content-Type": "application/json"
        },
                                    json={
                                        "name": "Тестовая группа селен12",
                                        "comment": "Создание группы через автотест1"
                                    })

        data_card_group = create_card_group.json()
        id_group = data_card_group['id']
        #print(id_group)
        print(data_card_group)

    with allure.step("Добавление карты в группу"):
        browser.open(f'groups/{id_group}')
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Поиск по номеру карты"]').type('***')
        time.sleep(1)
        browser.element('[class="flex checkbox"]').click() #выбрали карту
        browser.element('[class="btn btn--green"]').click() #клик добавить
        time.sleep(0.5)
        browser.element('[class="btn btn--green"]').click() #клик продолжить (инфа о переносе)
        time.sleep(0.5)
        browser.element('[class="btn btn--green"]').click() #вернуться к группе
        time.sleep(0.5)
        browser.element('[class="card-number"]').should(have.text('***'))
        #time.sleep(2)
    with allure.step("Удаление группы"):
        delete_group = requests.delete(url=swagger_url + f'contracts/{id_contract}/card-groups/{id_group}',
                                      headers=
                                      {
                                          "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                          "Content-Type": "application/json"
                                      })
        data_delete_group = delete_group.json()
        print(data_delete_group)

