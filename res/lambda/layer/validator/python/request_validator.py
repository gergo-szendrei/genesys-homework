import json
from body_validator import *


class RequestValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_request_create_user(event) -> dict:
    prefix = "Request validation failed! "
    if "body" not in event:
        raise RequestValidationException(prefix + "Body is mandatory!")
    body = json.loads(event["body"])
    validate_body_create_user(body)
    return body
