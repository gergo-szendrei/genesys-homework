import json
from body_validator import *


class RequestValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_request_create_user(event) -> dict:
    body = validate_request_common(event)
    validate_body_create_user(body)
    return body


def validate_request_update_user(event) -> dict:
    body = validate_request_common(event)
    validate_body_update_user(body)
    return body


def validate_request_common(event) -> dict:
    prefix = "Request validation failed! "
    if "body" not in event:
        raise RequestValidationException(prefix + "Body is mandatory!")
    return json.loads(event["body"])
