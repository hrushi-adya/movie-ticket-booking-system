import json
from model import constants
from model.LambdaResponse import DecimalEncoder, SimpleResponse
import logging
from cognito import CognitoIdentityProviderWrapper
from botocore.exceptions import ClientError
import boto3

from util.dynamodb_utilities import get_user_by_key

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
                    # response = sign_in_user(email, password)
                    user = get_user_by_key(email, email)
                    if user is None:
                        raise Exception('User does not exist')
                    elif user['user_id'] == email and user['password'] == password:
                        return {
                            'statusCode': 200,
                            'body': json.dumps({
                            'message': 'User Logged In Successfully',
                            'data': user  # Use DecimalEncoder in the outer json.dumps
                            }, cls=DecimalEncoder)
                        }
                    else:
                        return {
                            'statusCode': 401,
                            'body': json.dumps({
                                'message': 'Incorrect username or password'
                            })
                        }
                else:
                    Exception('Inaproppriate request body to sign in user')    
        except Exception as e:
            logger.error(f'Error processing request: {e}')
            raise Exception('Internal server error')
        
def sign_in_user(user_id:str, password:str):
    cognito_idp_client = boto3.client('cognito-idp', region_name='us-east-2')

    user_pool_id = constants.user_pool_id
    client_id = constants.client_id
    client_secret = constants.client_secret

    cognito = CognitoIdentityProviderWrapper(cognito_idp_client = cognito_idp_client, user_pool_id = user_pool_id, 
                                     client_id = client_id, client_secret = client_secret)
    
    try:
        response = cognito.start_sign_in(user_id, password)
    except ClientError as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message)
    return response
