from tests.models.ui_pages.page_create_limit_card import CardlimitPage

def test_create_card_limit(auth):
    page_limit = CardlimitPage()

    page_limit.open_page()
    page_limit.type_category_group_product('Нефтепродукты','Аи-95','Аи-95 Бренд')
    page_limit.type_limit('Разрешено с ограничениями')
    page_limit.type_summ_limit('4321')
    page_limit.type_period_limit('1', 'месяц')
    page_limit.type_additional_settings()
    page_limit.type_weedays(
        'понедельник',
        'вторник',
        'среда',
        'четверг',
        'пятница',
        'суббота',
        'воскресенье'
    )
    page_limit.type_time_limit('00002359')
    page_limit.type_number_transactions('321')
    page_limit.save_limit()
    page_limit.should_save_limit('Аи-95 Бренд')
    page_limit.delete_limit('Аи-95 Бренд')






