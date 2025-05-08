from tests.models.pages.page_userinfo import UserinfoPage

def test_auth(auth):
    page_lk = UserinfoPage()

    page_lk.open_page()
    page_lk.request_userinfo()
    page_lk.should_data()