from field_validator import *


class DictValidationException(Exception):
    def __init__(self, message, field):
        super().__init__("Dict validation failed! " + message)
        self.field = field


def validate_dict_create_user(dict_value: dict) -> None:
    if "full_name" not in dict_value:
        raise DictValidationException("Full name is mandatory!", "full_name")
    if "email_address" not in dict_value:
        raise DictValidationException("Email address is mandatory!", "email_address")
    if "password" not in dict_value:
        raise DictValidationException("Password is mandatory!", "password")

    validate_field_full_name(dict_value["full_name"])
    validate_field_email_address(dict_value["email_address"])
    validate_field_password(dict_value["password"])


def validate_dict_update_user(dict_value: dict) -> None:
    validate_dict_create_user(dict_value)
    validate_dict_common_uuid(dict_value)


def validate_dict_list_users(dict_value: dict) -> None:
    if "limit" not in dict_value:
        raise DictValidationException("Limit is mandatory!", "limit")

    validate_field_limit(dict_value["limit"])
    validate_dict_common_uuid(dict_value, True)


def validate_dict_common_uuid(dict_value: dict, value_optional=False) -> None:
    if "uuid" not in dict_value:
        raise DictValidationException("UUID is mandatory!", "uuid")

    criteria_a = not value_optional
    criteria_b = value_optional and dict_value["uuid"] is not None

    if criteria_a or criteria_b:
        validate_field_uuid(dict_value["uuid"])
