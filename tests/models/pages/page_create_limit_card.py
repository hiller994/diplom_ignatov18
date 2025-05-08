import allure
import requests
from selene import browser, have, be

from tests.website.conftest import swagger_url, id_card

class CardlimitPage:
    @allure.step('Открытие формы создания лимита')
    def open_page(self):
        browser.open(f"cards/{id_card}?tab=1")
        browser.element('[class="btn btn--fit btn--green"]').click()

    @allure.step('Выбор категории/группы/товара')
    def type_category_group_product(self, value_category, value_group, value_product):
        browser.element('//*[contains(@class, "select__value") and contains(text(), "Все категории")]').click()
        browser.element(f'//*[contains(@class, "select__option") and contains(text(), "{value_category}")]').click() #"Нефтепродукты"
        browser.element('//*[contains(@class, "select__value") and contains(text(), "Все группы")]').click()
        browser.element(f'//*[contains(@class, "select__option") and contains(text(), "{value_group}")]').click() #"Аи-95"
        browser.element('//*[contains(@class, "select__value") and contains(text(), "Все товары")]').click()
        browser.element(f'//*[contains(@class, "select__option") and contains(text(), "{value_product}")]').click() #"Аи-95 Бренд"

    @allure.step('Выбор типа ограничителя')
    def type_limit(self, value_type_limit):
        browser.all('.tn-select').element_by(have.text('Тип ограничителя')).element('.select__trigger').click()
        browser.element(
            f'//*[contains(@class, "select__option") and contains(text(), "{value_type_limit}")]').click() #"Разрешено с ограничениями"

    @allure.step('Указание суммы лимита')
    def type_summ_limit(self, value_summ_limit):
        browser.element('[placeholder="Укажите сумму"]').type(value_summ_limit)

    @allure.step('Указание периода лимита')
    def type_period_limit(self, value_number, value_period):
        browser.all('.input-group').element_by(have.text('Период')).element('[type="number"]').type(value_number) #3
        browser.element(
            '//div[contains(@class, "input-group")][.//label[contains(., "Период")]]''/following-sibling::div[contains(@class, "tn-select")]''//div[@class="select__trigger"]').should(
            be.clickable).click()
        browser.element(f'//*[contains(@class, "select__option") and contains(text(), "{value_period}")]').click() # "месяц"

    @allure.step('Открытие дополнительных настроек')
    def type_additional_settings(self):
        browser.element('[class="flex checkbox"]').click()

    @allure.step('Доп. настройки. Выбор дней')
    def type_weedays(self, value_day1, value_day2, value_day3, value_day4, value_day5, value_day6, value_day7):
        browser.all('.tn-select').element_by(have.text('Дни недели')).element('.select__trigger').click()
        browser.element(f'//*[contains(text(), " {value_day1}")]').click() # понедельник
        browser.element(f'//*[contains(text(), " {value_day2}")]').click() # вторник
        browser.element(f'//*[contains(text(), " {value_day3}")]').click() # среда
        browser.element(f'//*[contains(text(), " {value_day4}")]').click() # четверг
        browser.element(f'//*[contains(text(), " {value_day5}")]').click() # пятница
        browser.element(f'//*[contains(text(), " {value_day6}")]').click() # суббота
        browser.element(f'//*[contains(text(), " {value_day7}")]').click() # воскресенье
        browser.element('[class="select-outside"]').click()

    @allure.step('Доп. настройки. Указание временного интервала лимита')
    def type_time_limit(self, value_time):
        browser.element('[placeholder="Укажите время"]').type(value_time) #00002359

    @allure.step('Доп. настройки. Указание кол-ва транзакций')
    def type_number_transactions(self, value_number_transactions):
        browser.element('[placeholder="Укажите ограничение по сумме"]').type(value_number_transactions) #123

    @allure.step('Сохранение оператора и возврат к списку')
    def save_limit(self):
        browser.element('[class="btn btn--green"]').click() # сохранение
        browser.element('[class="btn btn--green"]').click() # возврат к списку

    @allure.step('Проверка появления лимита в списке')
    def should_save_limit(self, value_product):
        browser.element(f'//*[contains(@class, "time") and contains(text(), " {value_product}")]').click() # Аи-95 Бренд

    @allure.step('Удаление лимита')
    def delete_limit(self, value_product):

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

        # Вариант 1: Простой перебор (если список небольшой)
        target_name = value_product # Аи-95 Бренд
        for item in data_card_limit:
            if item['title'] == target_name:
                limit_id = item['id']
                break
        #print(limit_id)

        # Удаление транспорта
        delete_limit_card = requests.delete(url=swagger_url + f'cards/{id_card}/limits/{limit_id}',
                                           headers=
                                           {
                                               "Authorization": f"Bearer {auth_data['auth']['accessToken']}",
                                               "Content-Type": "application/json"
                                           })
        responce_delete_limit_card = delete_limit_card.json()
        print(responce_delete_limit_card)







