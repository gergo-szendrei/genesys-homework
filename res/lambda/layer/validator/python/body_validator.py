from field_validator import *


class BodyValidationException(Exception):
    def __init__(self, message, field):
        super().__init__(message)
        self.field = field


def validate_body_create_user(body: dict) -> None:
    prefix = "Body validation failed! "
    if "full_name" not in body:
        raise BodyValidationException(prefix + "Full name is mandatory!", "full_name")
    if "email_address" not in body:
        raise BodyValidationException(
            prefix + "Email address is mandatory!", "email_address"
        )
    if "password" not in body:
        raise BodyValidationException(prefix + "Password is mandatory!", "password")

    validate_field_full_name(body["full_name"])
    validate_field_email_address(body["email_address"])
    validate_field_password(body["password"])
