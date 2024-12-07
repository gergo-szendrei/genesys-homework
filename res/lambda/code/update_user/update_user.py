import boto3
import json

from request_validator import *
from dynamo_helper import *
from exist_validator import *
from hash_helper import *

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    print(context)

    try:
        body = validate_request_update_user(event)
        dynamo_result_uuid = get_user_by_uuid(dynamodb, body["uuid"])
        validate_present_user(dynamo_result_uuid)

        if (
            dynamo_result_uuid["Items"][0]["email_address"]["S"]
            != body["email_address"]
        ):
            dynamo_result_email_address = get_user_by_email_address(
                dynamodb, body["email_address"]
            )
            validate_unique_email_address(dynamo_result_email_address)

        hash_salt, hashed_password = hash_value(body["password"])
        update_user(
            dynamodb,
            body["uuid"],
            body["full_name"],
            body["email_address"],
            hash_salt,
            hashed_password,
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "uuid": body["uuid"],
                    "full_name": body["full_name"],
                    "email_address": body["email_address"],
                    "last_login": dynamo_result_uuid["Items"][0]["last_login"]["S"],
                }
            ),
        }
    except (
        FieldValidationException,
        BodyValidationException,
        RequestValidationException,
        ExistValidationException,
    ) as e:
        print(f"Error: {e}")
        return {"statusCode": 400, "body": json.dumps(str(e))}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps(str(e))}
