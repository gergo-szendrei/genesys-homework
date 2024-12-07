from simple_validator import *


class FieldValidationException(Exception):
    def __init__(self, message, field):
        super().__init__("Field validation failed! " + message)
        self.field = field


def validate_field_full_name(value: str) -> None:
    field = "full_name"
    prefix = "Full name "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_min_length(value, 3):
        raise FieldValidationException(prefix + "is too short!", field)
    if not is_max_length(value, 64):
        raise FieldValidationException(prefix + "is too long!", field)
    if not has_character(value, Character.space):
        raise FieldValidationException(prefix + "is invalid!", field)


def validate_field_email_address(value: str) -> None:
    field = "email_address"
    prefix = "Email address "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_min_length(value, 6):
        raise FieldValidationException(prefix + "is too short!", field)
    if not is_max_length(value, 64):
        raise FieldValidationException(prefix + "is too long!", field)
    if not is_email(value):
        raise FieldValidationException(prefix + "is invalid!", field)


def validate_field_password(value: str) -> None:
    field = "password"
    prefix = "Password "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_min_length(value, 12):
        raise FieldValidationException(prefix + "is too short!", field)
    if not is_max_length(value, 64):
        raise FieldValidationException(prefix + "is too long!", field)
    if not has_character(value, Character.upper):
        raise FieldValidationException(prefix + "must have uppercase letter!", field)
    if not has_character(value, Character.lower):
        raise FieldValidationException(prefix + "must have lowercase letter!", field)
    if not has_character(value, Character.number):
        raise FieldValidationException(prefix + "must have number!", field)
    if not has_character(value, Character.special):
        raise FieldValidationException(prefix + "must have special character!", field)


def validate_field_uuid(value: str) -> None:
    field = "uuid"
    prefix = "UUID "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_uuid(value):
        raise FieldValidationException(prefix + "is invalid!", field)


def validate_field_limit(value: int) -> None:
    if not is_min_value(value, 1):
        raise FieldValidationException("Limit is too small!", "limit")
