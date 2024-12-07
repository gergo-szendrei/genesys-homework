import boto3
import json

from request_validator import *
from dynamo_helper import *
from exist_validator import *

dynamodb = boto3.client("dynamodb")

# --- DEVELOPMENT POINT - BODY vs PARAM ---
# For this list logic, query params are also viable option
# In a production project I would most likely go with query params, but for this assignment I chose request body
# approach as it is already implemented


def lambda_handler(event, context):
    print(context)

    try:
        body = validate_request_list_users(event)

        dynamo_result_list = list_users(dynamodb, body["uuid"], body["limit"])
        response = []
        for user in dynamo_result_list["Items"]:
            response.append(
                {
                    "uuid": user["uuid"]["S"],
                    "full_name": user["full_name"]["S"],
                    "email_address": user["email_address"]["S"],
                    "last_login": user["last_login"]["S"],
                }
            )

        return {
            "statusCode": 200,
            "body": json.dumps(response),
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
