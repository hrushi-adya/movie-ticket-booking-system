import json
import logging
from json import JSONDecodeError

import boto3
from botocore.exceptions import ClientError
from model import constants
from cognito import CognitoIdentityProviderWrapper

from model.LambdaResponse import SimpleResponse
from util import dynamodb_utilities

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print("Event: ", event)
    if 'httpMethod' not in event:
        raise RuntimeError('No HttpMethod')
    logger.info("Event:")
    print(json.dumps(event))

    # if event['httpMethod'] == 'OPTIONS':
    #     return {
    #         'statusCode': 200,
    #         'headers': {
    #             'Access-Control-Allow-Origin': '*',
    #             'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    #             'Access-Control-Allow-Headers': 'Content-Type',
    #         },
    #         'body': ''
    #     }

    try:
        body = json.loads(event['body'])
    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except TypeError as e:
        raise TypeError('Error when decoding json body', inner=e)

    user_id = body["user_id"]
    password = body["password"]
    email_id = body["email"]
    phone = body["phone"]
    profile_type = body["profile_type"]
    first_name = body["first_name"]
    last_name = body["last_name"]

    # sign_up_user(user_id, profile_type, password, email_id, phone)
    #handle password and email id validation code in react js
    try:
        #check if user already present
        user = dynamodb_utilities.get_user_by_key(user_id, email_id)
        if user is not None:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'User already present'})
            }
        user = put_user_to_table(user_id, password, email_id, phone, profile_type, first_name, last_name)
    except Exception as e:
        logger.error(f'Error processing request: {e}')
        raise Exception('Internal server error')

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'message': 'User Sign Up Successful'
        })
    }


# Sign Up User API Call
def sign_up_user(user_id: str, profile_type: str, password: str, email_id: str, phone: str):
    cognito_idp_client = boto3.client('cognito-idp',
                                      region_name="us-east-2")

    user_pool_id = constants.user_pool_id
    client_id = constants.client_id
    client_secret = constants.client_secret

    # Setup Cognito utility client
    cognito = CognitoIdentityProviderWrapper(cognito_idp_client=cognito_idp_client, user_pool_id=user_pool_id,
                                             client_id=client_id, client_secret=client_secret)

    # Sign UP a user with email and phone number, authentication code will come to EMAIL.
    try:
        cognito.sign_up_user_ph(user_id, profile_type, password, email_id, phone)
    except Exception as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message, 400)


# Add User API Call
def put_user_to_table(user_id: str, password: str, email_id: str, phone: str,
                      profile_type: str, first_name: str, last_name: str):
    user = {}
    user["user_id"] = user_id
    user["password"] = password
    user["profile_type"] = profile_type
    user["first_name"] = first_name
    user["last_name"] = last_name
    user["email"] = email_id
    user["phone"] = phone
    user["watch_list"] = {}

    try:
        dynamodb_utilities.put_user(user)
    except ClientError as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message)

    return user
