import hashlib
import uuid


def hash_value(value) -> tuple:
    encoded_value = value.encode("utf-8")
    hash_salt = str(uuid.uuid4())
    encoded_salt = hash_salt.encode("utf-8")
    hashed_value = hashlib.sha512(encoded_value + encoded_salt).hexdigest()
    return hash_salt, hashed_value


def is_matching(value, hash_salt, check_hashed_value) -> bool:
    encoded_value = value.encode("utf-8")
    encoded_salt = hash_salt.encode("utf-8")
    hashed_value = hashlib.sha512(encoded_value + encoded_salt).hexdigest()
    return hashed_value == check_hashed_value
