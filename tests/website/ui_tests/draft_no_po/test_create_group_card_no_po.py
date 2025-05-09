import allure
import requests
from selene import browser, have, be

from tests.website.ui_tests.conftest import swagger_url, id_contract


def test_create_group_card():
    with allure.step("Выбор контракта для создания группы"):
        browser.open('cards?tab=2')
        #browser.element('[class="tn-select green"]').click()
        #browser.element('//*[contains(@class, "selected select__option") and contains(text(), "001-C-511391")]').click()
    with allure.step("Создание группы"):
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Введите название"]').type('Тестовая группа селен')
        browser.element('[placeholder="Введите примечание"]').type("Тестовое описание группы, созданное через автотест")
        browser.element('[class="btn btn--green"]').click()
    with allure.step("Проверка наименования созданной группы"):
        browser.element('[class="green"]').should(have.text('Тестовая группа селен'))
    with allure.step("Переход в группу"):
        browser.element('[class="btn btn--green"]').click()
        browser.element('//*[contains(text(), "Тестовое описание группы, созданное через автотест")]').should(be.visible)
    with allure.step("Запрос списка групп (для удаления)"):
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
        target_name_group = 'Тестовая группа селен'
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


