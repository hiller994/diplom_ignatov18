from tests.models.ui_pages.page_create_transport import TransportPage

def test_create_transport(auth):
    page_ts = TransportPage()

    page_ts.open_page()
    page_ts.type_brand_and_model('Тестмарка','Тестмодель')
    page_ts.select_country('Россия')
    page_ts.type_number('О221НН716')
    page_ts.save_transport()
    page_ts.should_save_transport('Тестмарка','О221НН716')
    page_ts.delete_transport('О221НН716')


