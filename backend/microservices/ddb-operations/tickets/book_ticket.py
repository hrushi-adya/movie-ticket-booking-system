import json
import logging
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from microservices.ses.send_email import send_email_ses
from util import dynamodb_utilities
from json import JSONDecodeError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print("Event: ", event)
    if 'httpMethod' not in event:
        raise RuntimeError('No HttpMethod')
    logger.info("Event:")
    logger.info(json.dumps(event))

    try:
        body = json.loads(event['body'])
    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except TypeError as e:
        raise TypeError('Error when decoding json body', inner=e)
    
    #ticket details dictionary
    ticket_id = uuid4().hex
    ticket_price = body["ticket_price"]
    ticket_quantity = body["ticket_quantity"]
    ticket_showtime = body["ticket_showtime"]
    ticket_movie_id = body["ticket_movie_id"]
    ticket_theater_id = body["ticket_theater_id"]
    ticket_user_id = body["ticket_user_id"]
    ticket_status = body["ticket_status"]
    ticket_transaction_id = body["ticket_transaction_id"]
    ticket_payment_status = body["ticket_payment_status"]
    
    ticket = add_ticket(ticket_id, ticket_price, ticket_quantity, ticket_showtime, ticket_movie_id, ticket_user_id, ticket_status, ticket_transaction_id, ticket_payment_status, ticket_theater_id)
    transaction = add_transaction(ticket_transaction_id, ticket_price, ticket_showtime, ticket_payment_status, ticket_user_id)
    # response = send_email_ses("Ticket booked successfully", ticket)
    if ticket is not None and transaction is not None:
        #send notification to user
        pass
    # Add method to send notification user for ticket booking using AWS SNS Service
    body['ticket_id'] = ticket_id
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Ticket booked successfully',
            'data1': body # Include the original input map and new ticket_id
            # 'email_response': response
        })
    }


def add_ticket(ticket_id, ticket_price, ticket_quantity, ticket_showtime, ticket_movie_id, ticket_user_id, ticket_status, ticket_transaction_id, ticket_payment_status, ticket_theater_id):
    ticket = {}
    ticket['ticket_id'] = ticket_id
    ticket['ticket_price'] = ticket_price
    ticket['ticket_quantity'] = ticket_quantity
    ticket['ticket_showtime'] = ticket_showtime
    ticket['ticket_movie_id'] = ticket_movie_id
    ticket['ticket_user_id'] = ticket_user_id
    ticket['ticket_status'] = ticket_status
    ticket['ticket_transaction_id'] = ticket_transaction_id
    ticket['ticket_payment_status'] = ticket_payment_status
    ticket['ticket_theatre_id'] = ticket_theater_id
    try:
        dynamodb_utilities.put_ticket(ticket)
    except ClientError as e:
        raise Exception('Error when adding ticket to DynamoDB', inner=e)
    return ticket

def add_transaction(transaction_id, transaction_amount, transaction_date, transaction_payment_status, transaction_user_id):
    transaction = {}
    transaction['transaction_id'] = transaction_id
    transaction['transaction_amount'] = transaction_amount
    transaction['transaction_date'] = transaction_date
    transaction['transaction_payment_status'] = transaction_payment_status
    transaction['transaction_user_id'] = transaction_user_id

    try:
        dynamodb_utilities.put_transaction(transaction)
    except ClientError as e:
        raise Exception('Error when adding transaction to DynamoDB', inner=e)
    return transaction
