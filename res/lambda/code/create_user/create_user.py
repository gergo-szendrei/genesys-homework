import boto3
import json
import uuid

from request_validator import *
from dynamo_helper import *
from exist_validator import *
from hash_helper import *

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    print(context)

    try:
        body = validate_request_create_user(event)
        dynamo_result_email_address = get_user_by_email_address(
            dynamodb, body["email_address"]
        )
        validate_exist_unique_email_address(dynamo_result_email_address)

        uuid_value = str(uuid.uuid4())
        hash_salt, hashed_password = hash_value(body["password"])
        save_user(
            dynamodb,
            uuid_value,
            body["full_name"],
            body["email_address"],
            hash_salt,
            hashed_password,
        )

        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "uuid": uuid_value,
                    "full_name": body["full_name"],
                    "email_address": body["email_address"],
                    "last_login": "",
                }
            ),
        }
    except (
        FieldValidationException,
        DictValidationException,
        RequestValidationException,
        ExistValidationException,
    ) as e:
        print(f"Error: {e}")
        return {"statusCode": 400, "body": json.dumps(str(e))}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps(str(e))}
