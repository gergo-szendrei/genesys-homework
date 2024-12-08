import boto3
import json
import datetime

from request_validator import *
from dynamo_helper import *
from exist_validator import *
from hash_helper import *

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    print(context)

    try:
        body = validate_request_login_user(event)
        dynamo_result_by_email_address = get_user_by_email_address(
            dynamodb, body["email_address"]
        )

        if dynamo_result_by_email_address["Count"] == 0 or not is_matching_hash(
            body["password"],
            dynamo_result_by_email_address["Items"][0]["salt"]["S"],
            dynamo_result_by_email_address["Items"][0]["password"]["S"],
        ):
            return {
                "statusCode": 401,
                "body": json.dumps("Invalid email address or password!"),
            }

        last_login = datetime.datetime.now().strftime("%Y.%m.%d %I:%M:%S.%f")
        update_last_login(
            dynamodb,
            dynamo_result_by_email_address["Items"][0]["uuid"]["S"],
            last_login,
        )

        # Generate auth token, cookie, etc. here and pass it back via response

        return {
            "statusCode": 200,
            "body": json.dumps({"token": "imagine_generated_token_here"}),
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
