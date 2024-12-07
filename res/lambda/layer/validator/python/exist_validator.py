class ExistValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_unique_email_address(dynamo_result) -> None:
    if dynamo_result["Count"] != 0:
        raise ExistValidationException(
            "Exist validation failed! Email address must be unique!"
        )


def validate_present_user(dynamo_result) -> None:
    if dynamo_result["Count"] != 1:
        raise ExistValidationException("Exist validation failed! User should exist!")
