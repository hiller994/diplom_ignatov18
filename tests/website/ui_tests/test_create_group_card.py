from tests.models.ui_pages.page_create_group_card import GroupcardPage

def test_create_group_card(auth):
    page_group = GroupcardPage()

    page_group.open_page()
    page_group.type_name_group_and_note(
        'Тестовая группа селен 2025',
        'Тестовое описание группы, созданное через автотест'
    )
    page_group.save_group()
    page_group.should_save_group('Тестовое описание группы, созданное через автотест')
    page_group.delete_group('Тестовая группа селен')


