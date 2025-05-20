from tests.models.ui_pages.page_create_operator import OperatorPage

def test_create_operator(auth):
    page_operator = OperatorPage()

    page_operator.open_page()
    page_operator.type_fio('Автотестов2309','Оператор','Тестович')
    page_operator.type_number('72056200525')
    page_operator.type_email('autotest23042025@gmail.com')
    page_operator.type_note('Тестовая заметка по оператору')
    page_operator.add_contract('001-C-511391')
    page_operator.save_opetator()
    page_operator.should_save_operator('Автотестов2309','autotest23042025@gmail.com')
    page_operator.delete_operator('Автотестов2309 Оператор Тестович')
