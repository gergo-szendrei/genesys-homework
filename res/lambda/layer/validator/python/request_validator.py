import json
from dict_validator import *


class RequestValidationException(Exception):
    def __init__(self, message):
        super().__init__("Request validation failed! " + message)


def validate_request_create_user(event) -> dict:
    body = validate_request_common_body(event)
    validate_dict_create_user(body)
    return body


def validate_request_update_user(event) -> dict:
    body = validate_request_common_body(event)
    validate_dict_update_user(body)
    return body


def validate_request_delete_user(event) -> dict:
    path_parameters = validate_request_common_path_parameters(event)
    validate_dict_common_uuid(path_parameters)
    return path_parameters


def validate_request_get_user(event) -> dict:
    path_parameters = validate_request_common_path_parameters(event)
    validate_dict_common_uuid(path_parameters)
    return path_parameters


def validate_request_list_users(event) -> dict:
    body = validate_request_common_body(event)
    validate_dict_list_users(body)
    return body


def validate_request_login_user(event) -> dict:
    body = validate_request_common_body(event)
    validate_dict_login_user(body)
    return body


def validate_request_common_body(event) -> dict:
    if "body" not in event:
        raise RequestValidationException("Body is mandatory!")
    return json.loads(event["body"])


def validate_request_common_path_parameters(event) -> dict:
    if "pathParameters" not in event:
        raise RequestValidationException("Path parameter is mandatory!")
    return event["pathParameters"]
