import json
import logging
from json import JSONDecodeError

from model.LambdaResponse import DecimalEncoder
from util.dynamodb_utilities import get_transaction_details

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print("Event: ", event)
    # if 'httpMethod' not in event:
    #     raise RuntimeError('No HttpMethod')
    if 'requestContext' not in event or 'http' not in event['requestContext']:
        raise RuntimeError('No HttpMethod or requestContext')
    http_method = event['requestContext']['http']['method']

    logger.info("Event:")
    logger.info(json.dumps(event))
    # http_method = event["httpMethod"]

    try:
        if http_method == "GET":
            if event['queryStringParameters'] is not None:
                start_date = event['queryStringParameters']['start_date']
                end_date = event['queryStringParameters']['end_date']

                print("start_date ", start_date)  
                print("end_date ", end_date)
                response = get_transaction_details(start_date, end_date) 
                print("response: ", response)
                return {
                    'statusCode': 200,
                    'body':  json.dumps(response, cls=DecimalEncoder)
                }
    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except Exception as e:
        raise Exception('Error when performing GET API', e)
