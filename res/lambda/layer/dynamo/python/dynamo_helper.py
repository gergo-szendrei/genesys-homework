import os


def get_user_by_email_address(dynamodb, email_address: str):
    return dynamodb.query(
        ExpressionAttributeValues={":email_address": {"S": email_address}},
        IndexName=os.environ["DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME"],
        KeyConditionExpression="email_address = :email_address",
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
    )


def get_user_by_uuid(dynamodb, uuid: str):
    return dynamodb.query(
        ExpressionAttributeNames={"#uuid": "uuid"},
        ExpressionAttributeValues={":uuid": {"S": uuid}},
        KeyConditionExpression="#uuid = :uuid",
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
    )


def list_users(dynamodb, uuid: str, limit: int):
    if uuid is None:
        return dynamodb.scan(
            Limit=limit,
            TableName=os.environ["DYNAMO_DB_USER_TABLE"],
        )

    return dynamodb.scan(
        ExclusiveStartKey={"uuid": {"S": uuid}},
        Limit=limit,
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
        Item={
            "uuid": {"S": uuid_value},
            "full_name": {"S": full_name},
            "email_address": {"S": email_address},
            "password": {"S": hashed_password},
            "salt": {"S": hash_salt},
            "last_login": {"S": ""},
        },
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
    )


def update_user(
    dynamodb,
    uuid_value: str,
    full_name: str,
    email_address: str,
    hash_salt: str,
    hashed_password: str,
) -> None:
    dynamodb.update_item(
        ExpressionAttributeValues={
            ":full_name": {"S": full_name},
            ":email_address": {"S": email_address},
            ":password": {"S": hashed_password},
            ":salt": {"S": hash_salt},
        },
        Key={"uuid": {"S": uuid_value}},
        ReturnValues="ALL_NEW",
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
        UpdateExpression="SET full_name = :full_name, email_address = :email_address, "
        + "password = :password, salt = :salt",
    )


def update_last_login(
    dynamodb,
    uuid_value: str,
    last_login: str,
) -> None:
    dynamodb.update_item(
        ExpressionAttributeValues={
            ":last_login": {"S": last_login},
        },
        Key={"uuid": {"S": uuid_value}},
        ReturnValues="ALL_NEW",
        TableName=os.environ["DYNAMO_DB_USER_TABLE"],
        UpdateExpression="SET last_login = :last_login",
    )


def delete_user(dynamodb, uuid_value: str) -> None:
    dynamodb.delete_item(
        Key={"uuid": {"S": uuid_value}}, TableName=os.environ["DYNAMO_DB_USER_TABLE"]
    )
