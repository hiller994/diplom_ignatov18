import allure
import requests
from selene import browser, have, be

from tests.website.ui_tests.conftest import swagger_url, id_card


def test_create_card_limit(auth):
    with allure.step("Открытие настроек карты"):
        browser.open(f"cards/{id_card}?tab=1")
        browser.element('[class="btn btn--fit btn--green"]').click()

    with allure.step("Выбор категории/группы/товара"):
        browser.element('//*[contains(@class, "select__value") and contains(text(), "Все категории")]').click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "Нефтепродукты")]').click()
        browser.element('//*[contains(@class, "select__value") and contains(text(), "Все группы")]').click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "Аи-95")]').click()
        browser.element('//*[contains(@class, "select__value") and contains(text(), "Все товары")]').click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "Аи-95 Бренд")]').click()

    with allure.step("Настройка ограничителей"):
        browser.all('.tn-select').element_by(have.text('Тип ограничителя')).element('.select__trigger').click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "Разрешено с ограничениями")]').click()
        browser.element('[placeholder="Укажите сумму"]').type('3333')
        browser.all('.input-group').element_by(have.text('Период')).element('[type="number"]').type('3')
        browser.element('//div[contains(@class, "input-group")][.//label[contains(., "Период")]]''/following-sibling::div[contains(@class, "tn-select")]''//div[@class="select__trigger"]').should(be.clickable).click()
        browser.element('//*[contains(@class, "select__option") and contains(text(), "месяц")]').click()
        #доп настройки лимита
        browser.element('[class="flex checkbox"]').click()
        browser.all('.tn-select').element_by(have.text('Дни недели')).element('.select__trigger').click()
        browser.element('//*[contains(text(), " понедельник")]').click()
        browser.element('//*[contains(text(), " вторник")]').click()
        browser.element('//*[contains(text(), " среда")]').click()
        browser.element('//*[contains(text(), " четверг")]').click()
        browser.element('//*[contains(text(), " пятница")]').click()
        browser.element('//*[contains(text(), " суббота")]').click()
        browser.element('//*[contains(text(), " воскресенье")]').click()
        browser.element('[class="select-outside"]').click()
        browser.element('[placeholder="Укажите время"]').type('00002359')
        browser.element('[placeholder="Укажите количество"]').type('3')
        browser.element('[placeholder="Укажите ограничение по сумме"]').type('234')
        browser.element('[class="btn btn--green"]').click()
        browser.element('[class="btn btn--green"]').click()

    with allure.step("Проверка создания лимита"):
        browser.element('//*[contains(@class, "time") and contains(text(), " Аи-95 Бренд")]').click()

    with allure.step("Получение лимитов по карте (для удаления)"):
        auth_data = browser.execute_script('''
                                            return {
                                                auth: JSON.parse(localStorage.getItem(".tn_gsb.tn_auth")),
                                                user: JSON.parse(localStorage.getItem(".tn_gsb.tn_user"))
                                            };
                                        ''')
        # отправляем запрос на получение лимитов
        requests_card_limit = requests.get(
            url=swagger_url + f'cards/{id_card}/limits/', headers=
            {
                "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                "Content-Type": "application/json"
            })
        data_card_limit = requests_card_limit.json()
        #print(data_card_limit)

    with allure.step("Получение id лимита по карте (для удаления)"):
        # Вариант 1: Простой перебор (если список небольшой)
        target_name = "Аи-95 Бренд"
        for item in data_card_limit:
            if item['title'] == target_name:
                limit_id = item['id']
                break
        #print(limit_id)


    with allure.step("Удаление лимита"):
        # Удаление транспорта
        delete_limit_card = requests.delete(url=swagger_url + f'cards/{id_card}/limits/{limit_id}',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                               "Content-Type": "application/json"
                                           })
        responce_delete_limit_card = delete_limit_card.json()
        print(responce_delete_limit_card)







