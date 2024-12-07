from field_validator import *


class DictValidationException(Exception):
    def __init__(self, message, field):
        super().__init__(message)
        self.field = field


def validate_body_create_user(body: dict) -> None:
    prefix = "Dict validation failed! "
    if "full_name" not in body:
        raise DictValidationException(prefix + "Full name is mandatory!", "full_name")
    if "email_address" not in body:
        raise DictValidationException(
            prefix + "Email address is mandatory!", "email_address"
        )
    if "password" not in body:
        raise DictValidationException(prefix + "Password is mandatory!", "password")

    validate_field_full_name(body["full_name"])
    validate_field_email_address(body["email_address"])
    validate_field_password(body["password"])


def validate_body_update_user(body: dict) -> None:
    validate_body_create_user(body)

    if "uuid" not in body:
        raise DictValidationException(
            "Dict validation failed! UUID is mandatory!", "uuid"
        )

    validate_field_uuid(body["uuid"])


def validate_path_parameters_delete_user(path_parameters: dict) -> None:
    if "uuid" not in path_parameters:
        raise DictValidationException(
            "Dict validation failed! UUID is mandatory!", "uuid"
        )

    validate_field_uuid(path_parameters["uuid"])
