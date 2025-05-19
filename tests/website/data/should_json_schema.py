import json

from jsonschema.validators import validate

from utils.file_path import path

#response - ответ запроса
#json_name - имя json схемы
def should_json(response, json_name):
    response_json = response.json()
    schema_path = path(json_name)
    with open(schema_path) as file:
        validate(response_json, schema=json.loads(file.read()))