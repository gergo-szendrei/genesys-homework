class ExistValidationException(Exception):
    def __init__(self, message):
        super().__init__("Exist validation failed! " + message)


def validate_exist_unique_email_address(dynamo_result) -> None:
    if dynamo_result["Count"] != 0:
        raise ExistValidationException("Email address must be unique!")


def validate_exist_present_user(dynamo_result) -> None:
    if dynamo_result["Count"] != 1:
        raise ExistValidationException("User should exist!")
