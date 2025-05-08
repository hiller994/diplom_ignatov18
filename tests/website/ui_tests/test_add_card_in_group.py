import time

import allure
import requests
from selene import browser, have

from tests.models.pages.page_add_card_in_group import AddcardgroupPage
from tests.website.conftest import swagger_url, id_contract


def test_add_card_in_group(auth):
    page_group = AddcardgroupPage()

    page_group.open_page()
    page_group.create_group()
    page_group.add_card_in_group('7013420000010785')
    page_group.save_card_in_group()
    page_group.should_card_in_group('7013420000010785')
    page_group.delete_group()

