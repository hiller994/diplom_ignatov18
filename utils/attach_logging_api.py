import json
import logging
from urllib.parse import urlparse

import allure
from allure_commons.types import AttachmentType


def attach_logging(request_variable):

# Получаем чистый путь
        full_url = request_variable.request.url

        logging.info(urlparse(full_url).path.lstrip('/'))
        logging.info(request_variable.status_code)
        logging.info(request_variable.text)

        # Декодируем body из bytes в str перед сохранением в allure
        request_body = request_variable.request.body.decode('utf-8') if request_variable.request.body else None

        allure.attach(
            body=request_body if request_body else "{}",  # На случай пустого тела
            name=f"Request body"
                f"Method: {request_variable.request.method}\n"
                f"Path: {urlparse(full_url).path.lstrip('/')}",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )

        allure.attach(body=json.dumps(request_variable.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")