from tests.models.pages.page_create_driver import DriverPage

def test_create_driver(auth):
    page_driver = DriverPage()

    page_driver.open_page()
    page_driver.type_fio('Автотестов','Водитель','Тестович')
    page_driver.type_number('72339050525')
    page_driver.type_note('Тестовое примечание при создании водителя')
    page_driver.add_card('7013420000010876')
    page_driver.save_driver()
    page_driver.should_save_driver('Автотестов','+7 233 905 05 25')
    page_driver.delete_driver('Автотестов Водитель Тестович')