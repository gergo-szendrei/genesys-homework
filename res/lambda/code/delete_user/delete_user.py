import boto3
import json

from request_validator import *
from dynamo_helper import *
from exist_validator import *

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    print(context)

    try:
        path_parameters = validate_request_delete_user(event)
        dynamo_result_uuid = get_user_by_uuid(dynamodb, path_parameters["uuid"])
        validate_present_user(dynamo_result_uuid)

        delete_user(dynamodb, path_parameters["uuid"])

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "uuid": path_parameters["uuid"],
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
