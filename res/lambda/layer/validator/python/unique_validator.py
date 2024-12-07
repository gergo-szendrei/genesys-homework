class UniqueValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_unique_create_user(dynamo_result) -> None:
    if dynamo_result["Count"] != 0:
        raise UniqueValidationException(
            "Unique validation failed! Email address must be unique!"
        )
