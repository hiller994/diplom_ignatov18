"""
- АВТОРИЗАЦИЯ API
- ШАГИ СОЗДАНИЯ И СОХРАЕНИЯ WEB
- УДАЛЕНИЕ API
"""


import allure
import requests
from selene import browser, have

from conftest import swagger_url, id_company


def test_create_driver():
    with allure.step("Cоздания оператора"):
        browser.open("drivers?tab=1")
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Введите фамилию"]').type('Автотестов1')
        browser.element('[placeholder = "Введите имя"]').type('Оператор2')
        browser.element('[placeholder="Введите отчество"]').type('Тестович3')
        browser.element('[placeholder = "Введите номер телефона"]').type('7***')
        browser.element('[placeholder="Введите адрес электронной почты"]').type('***@gmail.com')
        browser.element('[placeholder="Введите примечание"]').type('Создание через автотест')
        browser.element('[class ="btn btn--green"]').click()
        browser.element('//div[contains(@class, "item__flex") and contains(., "Ц***")]//*[contains(@class, "flex checkbox")]').click()
        '''
        //div[contains(@class, "item__flex") and contains(., "Товар1")] — ищет div с классом item__flex и текстом "Товар1".
        //*[contains(@class, "flex checkbox")] — внутри этого div ищет любой элемент с классом flex checkbox (чекбокс).
        '''
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="table__item"]').should(have.text('Автотестов1'))
        browser.element('//*[contains(@class, "mail") and contains(text(), "***@gmail.com")]').click()
        browser.element('[class="operator"]').should(have.text('Данные оператора'))
        #browser.element('[class="credentials"]').should(have.text('Автотестов Оператор Тест'))

    '''
    with allure.step("Удаление оператора (ui)"):
        browser.element('//div[contains(@class, "table__item") and contains(., "Автотестов1")]//*[contains(@class, "flex checkbox")]').click()
        browser.element('[class="link"]').click()
        browser.element('[class="btn btn--white"]').click()
        browser.element('[class="modal-title"]').should(have.text('Оператор удален'))
    '''

    with allure.step("Удаление оператора (api)"):
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
        target_fio = "Автотестов1 Оператор2 Тестович3"  # ФИО, которое ищем
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
