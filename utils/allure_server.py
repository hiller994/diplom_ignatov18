import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from path_env import ROOT

# Путь к .env.mobile относительно conftest.py
#env_path = Path(__file__).parent.parent.parent.parent / ".env.allure_server"
load_dotenv(os.path.join(ROOT, ".env.allure_server"))
#load_dotenv(".env.allure_server")

allure_login = os.getenv('ALLURE_LOGIN')
allure_pass = os.getenv('ALLURE_PASS')
allure_url_web = os.getenv('ALLURE_URL_WEB')
allure_url_swagger = os.getenv('ALLURE_URL_SWAGGER')
id_project = os.getenv('ALLURE_ID_PROJECT')

#print('login:', allure_login)
#print('pass:', allure_pass)


def post_allure_server_results():
    #создаём сессию
    session = requests.Session()

    # Логинимся
    response_login = session.post(
        url=allure_url_swagger + '/login',
        json={
            "username": allure_login,
            "password": allure_pass
        }
    )

    # Проверка успешного входа
    if response_login.status_code != 200:
        raise Exception(f"Login failed: {response_login.text}")

    # Чистка истории (удаление старых результатов)
    response_clean_history = session.get(
        url= allure_url_swagger + f'/clean-history?project_id={id_project}'
    )

    # Чистка результатов (удаление старых результатов)
    response_clean_results = session.get(
        url=allure_url_swagger + f'/clean-results?project_id={id_project}'
    )


    # Подготовка файлов
    results_dir = os.path.join(ROOT, "allure-results")
    file_paths = [
        os.path.join(results_dir, f)
        for f in os.listdir(results_dir)
        if os.path.isfile(os.path.join(results_dir, f))
    ]

    files = []

    try:
        for path in file_paths:
            file_name = os.path.basename(path)
            f = open(path, 'rb')
            files.append(('files[]', (file_name, f)))

        # Отправка результатов на сервер
        response_post = session.post(
            url=allure_url_swagger + '/send-results',
            params={
                "project_id": id_project,
                "force_project_creation": "false"
            },
            headers={
                "X-CSRF-TOKEN": session.cookies.get("csrf_access_token", ""),
                "accept": "*/*"
            },
            files=files
        )

        #print(f"Send results status: {response_post.status_code}")
        #print("Response:", response_post.text)

        # генерация результата на сервере
        response_generate_report = session.get(
            url=allure_url_swagger + '/generate-report?project_id=b2b-lk-ui&execution_name=Allure%20Docker%20Service%20UI'
        )

    finally:
        for _, (_, f) in files:
            f.close()

    #print("Responce clean history: ", response_clean_history.text)
    #print("Responce clean results: ", response_clean_results.text)

    #print("Status code login:", response_login.status_code)
    #print("Status code clean history: ", response_clean_history.status_code)
    #print("Status code clean results: ", response_clean_results.status_code)
    #print("Status code post file:", response_post.status_code)
    #print("Status code generate report:", response_generate_report.status_code)
    #print("Response post file:", response_post.text)
    #print("Responce generate: ", response_generate_report.text)

    '''
    # Путь к файлу с результатами
    file_path = "C:/diplom_ignatov18/tests/website/ui_tests/allure-results/f915de91-790d-4f54-bea4-9ac2dc092956-result.json"

    # Открываем файл в бинарном режиме УЖЕ ПОСЛЕ создания сессии
    with open(file_path, 'rb') as f:
        files = {
            'files[]': (
                'f915de91-790d-4f54-bea4-9ac2dc092956-result.json',  # Должно совпадать с реальным именем файла
                f,  # Передаём файловый объект, а не f.read()
                'application/json'
            )
        }
    '''