import os


def get_user_by_email_address(dynamodb, email_address: str):
    return dynamodb.query(
        ExpressionAttributeValues={":email_address": {"S": email_address}},
        IndexName=os.environ["DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME"],
        KeyConditionExpression="email_address = :email_address",
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
    )


def save_user(
    dynamodb,
    uuid_value: str,
    full_name: str,
    email_address: str,
    hash_salt: str,
    hashed_password: str,
) -> None:
    dynamodb.put_item(
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
        Item={
            "uuid": {"S": uuid_value},
            "full_name": {"S": full_name},
            "email_address": {"S": email_address},
            "password": {"S": hashed_password},
            "salt": {"S": hash_salt},
            "last_login": {"S": ""},
        },
    )
