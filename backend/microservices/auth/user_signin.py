import json
from model import constants
from model.LambdaResponse import SimpleResponse
import logging
from cognito import CognitoIdentityProviderWrapper
from botocore.exceptions import ClientError
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
        
        if 'httpMethod' not in event:
            raise Exception('No httpMethod')
    
        logger.info('Event:')
        logger.info(json.dumps(event))
        http_method = event['httpMethod']
        
        try:
            if http_method == 'POST':
                body = json.loads(event['body'])
                if all(k in body for k in ('user_id', 'password')):
                    email = body['user_id']
                    password = body['password']
                    response = sign_in_user(email, password)
                    return SimpleResponse({
                        'sign_in_status': response
                    })
                else:
                    Exception('Inaproppriate request body to sign in user')    
        except Exception as e:
            logger.error(f'Error processing request: {e}')
            raise Exception('Internal server error')
        
def sign_in_user(user_id:str, password:str):
    cognito_idp_client = boto3.client('cognito-idp', region_name='us-east-1')

    user_pool_id = constants.USER_POOL_ID
    client_id = constants.CLIENT_ID
    client_secret = constants.CLIENT_SECRET

    cognito = CognitoIdentityProviderWrapper(cognito_idp_client = cognito_idp_client, user_pool_id = user_pool_id, 
                                     client_id = client_id, client_secret = client_secret)
    
    try:
        response = cognito.sign_in_user(user_id, password)
    except ClientError as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message)
    return response
