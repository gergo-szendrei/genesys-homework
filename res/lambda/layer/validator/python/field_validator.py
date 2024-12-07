from simple_validator import *


class FieldValidationException(Exception):
    def __init__(self, message, field):
        super().__init__(message)
        self.field = field


def validate_field_full_name(value) -> None:
    field = "full_name"
    prefix = "Field validation failed! Full name "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_min_length(value, 3):
        raise FieldValidationException(prefix + "is too short!", field)
    if not is_max_length(value, 64):
        raise FieldValidationException(prefix + "is too long!", field)
    if not has_character(value, Character.space):
        raise FieldValidationException(prefix + "is invalid!", field)


def validate_field_email_address(value) -> None:
    field = "email_address"
    prefix = "Field validation failed! Email address "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_min_length(value, 6):
        raise FieldValidationException(prefix + "is too short!", field)
    if not is_max_length(value, 64):
        raise FieldValidationException(prefix + "is too long!", field)
    if not is_email(value):
        raise FieldValidationException(prefix + "is invalid!", field)


def validate_field_password(value) -> None:
    field = "password"
    prefix = "Field validation failed! Password "
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
    prefix = "Field validation failed! UUID "
    if not is_provided(value):
        raise FieldValidationException(prefix + "is mandatory!", field)
    if not is_uuid(value):
        raise FieldValidationException(prefix + "is invalid!", field)
