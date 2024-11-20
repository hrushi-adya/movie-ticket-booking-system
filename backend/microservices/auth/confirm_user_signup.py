
import json
import logging
from botocore.exceptions import ClientError
from cognito import CognitoIdentityProviderWrapper
import boto3
from model import constants
from model.LambdaResponse import SimpleResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    if 'httpMethod' not in event:
        raise Exception('No httpMethod')

    logger.info('Event:')
    logger.info(json.dumps(event))
    http_method = event['httpMethod']
    
    try:
        if http_method == 'GET':
            user_id = event['queryStringParameters']['user_id']
            logger.info(f'Sending confirmation code for the user id:{user_id}')
            response = resend_confirmation_code(user_id)
            return SimpleResponse({
                'conformation_code_details': response
            })
        elif http_method == 'POST':
            body = json.loads(event['body'])
            if all(k in body for k in ('code', 'user_id')):
                code = body['code']
                user_id = body['user_id']
                response = verify_sign_up_user(code, user_id)
                return SimpleResponse({
                    'verification_status': response
                })
            else:
                Exception('Inaproppriate request body to verify user sign up')    
    except Exception as e:
        logger.error(f'Error processing request: {e}')
        raise Exception('Internal server error')
    
def resend_confirmation_code(user_id:str):
    cognito_idp_client = boto3.client('cognito-idp', region_name='us-east-2')

    user_pool_id = constants.user_pool_id
    client_id = constants.client_id
    client_secret = constants.client_secret

    cognito = CognitoIdentityProviderWrapper(cognito_idp_client = cognito_idp_client, user_pool_id = user_pool_id, 
                                     client_id = client_id, client_secret = client_secret)
    
    try:
        response = cognito.resend_confirmation(user_id)
    except ClientError as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message)
    return response

def verify_sign_up_user(code:str, user_id:str):
    cognito_idp_client = boto3.client('cognito-idp', region_name='us-east-2')

    user_pool_id = constants.user_pool_id
    client_id = constants.client_id
    client_secret = constants.client_secret

    cognito = CognitoIdentityProviderWrapper(cognito_idp_client = cognito_idp_client, user_pool_id = user_pool_id, 
                                     client_id = client_id, client_secret = client_secret)
    
    try:
        response = cognito.confirm_user_sign_up(code, user_id)
    except ClientError as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message)
    return response
