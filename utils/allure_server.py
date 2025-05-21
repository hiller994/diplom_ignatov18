import os
import requests
from dotenv import load_dotenv
from path_env import ROOT




load_dotenv(os.path.join(ROOT, ".env.allure_server"))

allure_login = os.getenv('ALLURE_LOGIN')
allure_pass = os.getenv('ALLURE_PASS')
allure_url_web = os.getenv('ALLURE_URL_WEB')
allure_url_swagger = os.getenv('ALLURE_URL_SWAGGER')
id_project = os.getenv('ALLURE_ID_PROJECT')


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

        # генерация результата на сервере
        response_generate_report = session.get(
            url=allure_url_swagger + f'/generate-report?project_id={id_project}&execution_name=Allure%20Docker%20Service%20UI'
        )

    finally:
        for _, (_, f) in files:
            f.close()