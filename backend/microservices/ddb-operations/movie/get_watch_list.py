import json
import logging
from json import JSONDecodeError

from model.LambdaResponse import DecimalEncoder
from util.dynamodb_utilities import get_user_by_key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print("Event: ", event)
    if 'httpMethod' not in event:
        raise RuntimeError('No HttpMethod')
    logger.info("Event:")
    logger.info(json.dumps(event))
    http_method = event["httpMethod"]

    try:
        if http_method == "GET":
            if event['queryStringParameters'] is not None:
                user_id = event['queryStringParameters']['user_id']
                print("user_id ", user_id)
                user = get_user_by_key(user_id, user_id)
                print("user: ", user)
                response = user['watch_list']
                print("response: ", response)
                return {
                    'statusCode': 200,
                    'body':  json.dumps(response, cls=DecimalEncoder)
                }
    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except Exception as e:
        raise Exception('Error when performing GET API', e)
