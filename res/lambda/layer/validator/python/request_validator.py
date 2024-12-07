import json
from dict_validator import *


class RequestValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_request_create_user(event) -> dict:
    body = validate_request_body(event)
    validate_body_create_user(body)
    return body


def validate_request_update_user(event) -> dict:
    body = validate_request_body(event)
    validate_body_update_user(body)
    return body


def validate_request_delete_user(event) -> dict:
    path_parameters = validate_request_path_parameters(event)
    validate_path_parameters_common_uuid(path_parameters)
    return path_parameters


def validate_request_get_user(event) -> dict:
    path_parameters = validate_request_path_parameters(event)
    validate_path_parameters_common_uuid(path_parameters)
    return path_parameters


def validate_request_body(event) -> dict:
    if "body" not in event:
        raise RequestValidationException(
            "Request validation failed! Body is mandatory!"
        )
    return json.loads(event["body"])


def validate_request_path_parameters(event) -> dict:
    if "pathParameters" not in event:
        raise RequestValidationException(
            "Request validation failed! Path parameter is mandatory!"
        )
    return event["pathParameters"]
