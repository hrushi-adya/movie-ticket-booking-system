import os

import boto3
from util.utilities import generate_utc_timestamp, update


def put_user(user: dict):
    """
    Put (create) a new user

    :param user:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        # hexed_user_key = generate_unique_key('user_key_cur', hexing=True)
        print(f"User Key assigned: {user['user_id']}")

        # Update metadata
        timestamp = generate_utc_timestamp()
        update(user, {
            'created_at': timestamp,
            'updated_at': timestamp
        })

        table = dynamodb.Table(os.environ.get("USER_TABLE"))

        table.put_item(Item={
            **user
        })

        return {
            'key': user['user_id']
        }
    except Exception as e:
        raise Exception('Error querying DynamoDB when put an user')
