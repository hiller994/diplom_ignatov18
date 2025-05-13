import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# Путь к .env.mobile относительно conftest.py
env_path = Path(__file__).parent.parent.parent.parent / ".env.allure_server"
load_dotenv(env_path)

allure_login = os.getenv('ALLURE_LOGIN')
allure_pass = os.getenv('ALLURE_PASS')
allure_url_web = os.getenv('ALLURE_URL_WEB')
allure_url_swagger = os.getenv('ALLURE_URL_SWAGGER')

print('login:', allure_login)
print('pass:', allure_pass)


def test_post_allure_server_results():
    # Сначала выполняем логин и создаём сессию
    session = requests.Session()

    # Логинимся
    response_login = session.post(
        url=allure_url_swagger + '/login',
        json={
            "username": os.getenv('ALLURE_LOGIN'),
            "password": os.getenv('ALLURE_PASS')
        }
    )

    # Проверка успешного входа
    if response_login.status_code != 200:
        raise Exception(f"Login failed: {response_login.text}")

    # Путь к файлу с результатами
    file_path = "C:/diplom_ignatov18/tests/website/ui_tests/allure-results/e14cc012-ffe8-4e69-ab26-af23b8aa34b8-result.json"

    # Открываем файл в бинарном режиме УЖЕ ПОСЛЕ создания сессии
    with open(file_path, 'rb') as f:
        files = {
            'files[]': (
                '231580e4-f716-4858-96ce-c3ed64484df5-result.json',  # Должно совпадать с реальным именем файла
                f,  # Передаём файловый объект, а не f.read()
                'application/json'
            )
        }

        response_post_file = session.post(
            url=allure_url_swagger +  '/send-results',
            params={
                "project_id": 'b2b-lk-ui',
                "force_project_creation": "false"
            },
            headers={
                "X-CSRF-TOKEN": session.cookies.get("csrf_access_token", ""),
                "accept": "*/*"
            },
            files=files
        )

    print("Status code:", response_post_file.status_code)
    print("Response:", response_post_file.text)









'''
session = requests.Session()
response_login = requests.post(
    url='http://10.240.25.54:5050/allure-docker-service/login',
    json={
        "username": "admin",
        "password": "7B05BD6AEE"
    }

)
# Проверка успешного входа
if response_login.status_code != 200:
    raise Exception(f"Login failed: {response_login.text}")

# Куки будут автоматически сохранены в сессии

session.cookies.update(response_login.cookies)




# Путь к файлу с результатами
file_path = "C:/diplom_ignatov18/tests/website/ui_tests/allure-results/231580e4-f716-4858-96ce-c3ed64484df5-result.json"

# Открываем файл в бинарном режиме
with open(file_path, 'rb') as f:
    files = {
        'files[]': (  # Ключ должен соответствовать ожидаемому сервером
            '32ccb214-852d-434a-8d4c-7bcf8edcbc4f-result.json',  # Имя файла
            f.read(),  # Содержимое файла
            'application/json'  # MIME-тип
        )
    }




response_post_file = session.post(
    url=f'http://10.240.25.54:5050/allure-docker-service/send-results',
    params= {
        "project_id": 'b2b-lk-ui',
        "force_project_creation": "false"
    },
    headers={
        "X-CSRF-TOKEN": session.cookies.get("csrf_access_token", ""),
        "Content-Type": "multipart/form-data",
        "accept": "*/*"
    },
    files=files
)

print("Status code:",response_post_file.status_code)
print("Response:",response_post_file.text)
'''