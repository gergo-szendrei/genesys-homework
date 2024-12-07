import re
import uuid
from enum import Enum


class Character(Enum):
    space = "space"
    lower = "lower"
    upper = "upper"
    number = "number"
    special = "special"


def is_provided(value: str) -> bool:
    return value is not None and value.strip() != ""


def is_min_length(value: str, min_length: int) -> bool:
    return len(value) >= min_length


def is_max_length(value: str, max_length: int) -> bool:
    return len(value) <= max_length


def is_email(value: str) -> bool:
    return re.match(r"^[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value)


def is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def is_min_value(value: int, min_value: int) -> bool:
    return value >= min_value


def has_character(value: str, character: Character) -> bool:
    return len(get_matching_characters(value, character)) > 0


def get_matching_characters(value: str, character: Character) -> list:
    if character == Character.space:
        return [el for el in value if el.isspace()]
    if character == Character.lower:
        return [el for el in value if el.islower()]
    if character == Character.upper:
        return [el for el in value if el.isupper()]
    if character == Character.number:
        return [el for el in value if el.isdigit()]
    if character == Character.special:
        return [el for el in value if not el.isalnum()]
    raise Exception("Invalid character!", character)
