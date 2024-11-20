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

def get_user_by_key(user_id: str, email: str):
    """
    Get an user by key
    :param profile_type:
    :param profile_id:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get("USER_TABLE"))
        dynamodb_res = table.get_item(Key={'user_id': user_id, 'email': email})
        if 'Item' not in dynamodb_res:
            return None
        item = dynamodb_res['Item']
        
        return item
    except Exception as e:
        raise Exception('Error while getting user from table')

def update_user(user: dict):
    """
    Update an existing user

    :param user:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get("USER_TABLE"))

        # Update metadata
        timestamp = generate_utc_timestamp()
        update(user, {
            'updated_at': timestamp
        })

        table.update_item(
            Key={'user_id': user['user_id'], 'email': user['email']},
            UpdateExpression="set #name = :name, #email = :email, #updated_at = :updated_at",
            ExpressionAttributeNames={
                '#name': 'name',
                '#email': 'email',
                '#updated_at': 'updated_at'
            },
            ExpressionAttributeValues={
                ':name': user['name'],
                ':email': user['email'],
                ':updated_at': timestamp
            }
        )

        return {
            'key': user['user_id']
        }
    except Exception as e:
        raise Exception('Error updating user in DynamoDB')


def put_movie(movie: dict):
    """
    Add (create) a new movie

    :param user:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        # hexed_user_key = generate_unique_key('user_key_cur', hexing=True)
        print(f"User Key assigned: {movie['movie_id']}")

        # Update metadata
        timestamp = generate_utc_timestamp()
        update(movie, {
            'created_at': timestamp,
            'updated_at': timestamp
        })

        table = dynamodb.Table(os.environ.get("MOVIE_TABLE"))

        table.put_item(Item={
            **movie
        })

        return {
            'key': movie['movie_id']
        }
    except Exception as e:
        raise Exception('Error querying DynamoDB when put a movie')

def get_movie_by_key(movie_id: str):
    """
    Get an movie by key
    :param profile_type:
    :param profile_id:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get("MOVIE_TABLE"))
        dynamodb_res = table.get_item(Key={'movie_id': movie_id})
        if 'Item' not in dynamodb_res:
            return None
        item = dynamodb_res['Item']
        
        return item
    except Exception as e:
        raise Exception('Error while getting movie from table')

def put_ticket(ticket: dict):
    """
    Put (create) a new ticket

    :param user:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        # hexed_user_key = generate_unique_key('user_key_cur', hexing=True)
        print(f"User Key assigned: {ticket['ticket_id']}")

        # Update metadata
        timestamp = generate_utc_timestamp()
        update(ticket, {
            'created_at': timestamp,
            'updated_at': timestamp
        })

        table = dynamodb.Table(os.environ.get("TICKET_TABLE"))

        table.put_item(Item={
            **ticket
        })

        return {
            'key': ticket['ticket_id']
        }
    except Exception as e:
        raise Exception('Error querying DynamoDB when put a ticket')

def put_transaction(transaction: dict):
    """
    Put (create) a new transaction

    :param user:
    :return:
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        # hexed_user_key = generate_unique_key('user_key_cur', hexing=True)
        print(f"User Key assigned: {transaction['transaction_id']}")

        # Update metadata
        timestamp = generate_utc_timestamp()
        update(transaction, {
            'created_at': timestamp,
            'updated_at': timestamp
        })

        table = dynamodb.Table(os.environ.get("TRANSACTION_TABLE"))

        table.put_item(Item={
            **transaction
        })

        return {
            'key': transaction['transaction_id']
        }
    except Exception as e:
        raise Exception('Error querying DynamoDB when put a transaction')
