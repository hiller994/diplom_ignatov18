import allure
import requests
from selene import browser, have

from tests.website.conftest import id_company, swagger_url


def test_create_driver():
    with allure.step("Cоздание водителя"):
        browser.open("drivers?tab=0")
        browser.element('[class="btn btn--fit btn--green"]').click()
        browser.element('[placeholder="Введите фамилию"]').type('Автотестов')
        browser.element('[placeholder = "Введите имя"]').type('Водитель')
        browser.element('[placeholder="Введите отчество"]').type('Тестович')
        browser.element('[placeholder = "Введите номер телефона"]').type('7***')
        browser.element('[placeholder="Введите примечание"]').type('Создание через автотест')
        browser.element('[class ="btn btn--green"]').click()
        browser.element('[class="c-red"]').click()
        browser.element('[class="btn btn--green"]').click()
    with allure.step("Проверка сохранения водителя"):
        browser.element('[class="table__item"]').should(have.text('Автотестов'))
        browser.element('//*[contains(@class, "phone") and contains(text(), "+7 *** *** ** **")]').click()
        browser.element('[class="driver"]').should(have.text('Данные водителя'))
    with allure.step("Запрос на список водителей (для удаления)"):
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
        target_fio = "Автотестов Водитель Тестович"  # ФИО, которое ищем
        driver_id = None

        # Проверяем наличие ключа 'items' в ответе
        if 'items' in data_drivers:
            # Перебираем всех водителей
            for user in data_drivers['items']:
                # Проверяем совпадение ФИО (с учетом регистра)
                if user.get('fio') == target_fio:
                    driver_id = user['id']
                    break
    with allure.step("Удаление водителя"):
        #Удаление водителя
        delete_driver = requests.delete(url=swagger_url + f'companies/{id_company}/drivers/?driver_id={driver_id}',
                                      headers=
                                      {
                                          "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                          "Content-Type": "application/json"
                                      })
        responce_delete_drive = delete_driver.json()
        print(responce_delete_drive)


