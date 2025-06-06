import os

import boto3
from util.utilities import generate_utc_timestamp, update
from boto3.dynamodb.conditions import Attr


def put_user(user: dict):
    
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
    
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get("USER_TABLE"))
    
        print("user: ", user)
        # Update metadata
        # timestamp = generate_utc_timestamp()
        # update(user, {
        #     'updated_at': timestamp
        # })
        
        update_expression = "SET " + ", ".join(f"{key} = :{key}" for key in user.keys())
        expression_attribute_values = {f":{key}": value for key, value in user.items()}
        expression_attribute_names = {f"#{key}": key for key in user.keys()} 
        
        response = dynamodb.Table(os.environ.get("USER_TABLE")).put_item(Item={
            'user_id': user['user_id'],
            'email': user['email'],
            **user
        })

        return response
    except Exception as e:
        raise Exception('Error updating user in DynamoDB')


def put_movie(movie: dict):
    
    try:
        dynamodb = boto3.resource('dynamodb')
        # hexed_user_key = generate_unique_key('user_key_cur', hexing=True)
        print(f"User Key assigned: {movie['movie_name']}")

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
            'key': movie['movie_name']
        }
    except Exception as e:
        raise Exception('Error querying DynamoDB when put a movie')

def put_ticket(ticket: dict):
    
    try:
        dynamodb = boto3.resource('dynamodb')
        # hexed_user_key = generate_unique_key('user_key_cur', hexing=True)
        print(f"Ticket Key assigned: {ticket['ticket_id']}")

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

# Movie Methods
def get_movie(movie_id):
    dynamodb = boto3.resource('dynamodb')
       
    table = dynamodb.Table(os.environ.get("MOVIE_TABLE"))

    try:
        response = table.get_item(
            Key={
                'movie_name': movie_id
            }
        )
        if 'Item' in response:
            return response['Item']
    except Exception as e:
        print(e.response['Error']['Message'])
        return None

def get_movies():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get("MOVIE_TABLE"))

    try:
        response = table.scan()
        return response['Items']
    except Exception as e:
        print(e.response['Error']['Message'])
        return None

def delete_movie(movie_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get("MOVIE_TABLE"))
    try:
        response = table.delete_item(
            Key={
                'movie_name': movie_name
            }
        )
        return response
    except Exception as e:
        print(e.response['Error']['Message'])
        return None

def update_movie(movie_name:str, movie: dict):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get("MOVIE_TABLE"))
    
    update_expression = "SET " + ", ".join(f"{key} = :{key}" for key in movie.keys())
    expression_attribute_values = {f":{key}": value for key, value in movie.items()}

    try:
        response = table.update_item(
            Key={
                'movie_name': movie_name,
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        print(e.response['Error']['Message'])
        return None
    
def get_transaction_details(start_date, end_date):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get("TRANSACTION_TABLE"))
    try:
        response = table.scan(
            FilterExpression=Attr('transaction_date').between(start_date, end_date)
        )
        return response['Items']
    except Exception as e:
        print(e.response['Error']['Message'])
        return None