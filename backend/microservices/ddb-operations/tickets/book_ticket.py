import json
import logging
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from microservices.ses.send_email import send_email_ses
from util import dynamodb_utilities
from json import JSONDecodeError

from util.utilities import create_watchlist_node

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
    ticket_transaction_id = ticket_id
    ticket_payment_status = "confirmed"

    ticket = add_ticket(ticket_id, ticket_price, ticket_quantity, ticket_showtime, ticket_movie_id, ticket_user_id, ticket_status, ticket_transaction_id, ticket_payment_status, ticket_theater_id)
    if ticket:
        ticket_booked = True
        movie = dynamodb_utilities.get_movie(ticket_movie_id)
        print("movie: ", movie)
        update_movie_for_booking(movie, ticket_movie_id, ticket_booked, ticket_price, ticket_quantity)

    transaction = add_transaction(ticket_transaction_id, ticket_price, ticket_showtime, ticket_payment_status, ticket_user_id, ticket_movie_id)
    user = dynamodb_utilities.get_user_by_key(ticket_user_id, ticket_user_id)
    print("user: ", user)
    user = update_user_watchlist(user, ticket, ticket_id)
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

def add_transaction(transaction_id, transaction_amount, transaction_date, transaction_payment_status, transaction_user_id, trasaction_movie_id):
    transaction = {}
    transaction['transaction_id'] = transaction_id
    transaction['transaction_amount'] = transaction_amount
    transaction['transaction_date'] = transaction_date
    transaction['transaction_payment_status'] = transaction_payment_status
    transaction['transaction_user_id'] = transaction_user_id
    transaction['transaction_movie_id'] = trasaction_movie_id

    try:
        dynamodb_utilities.put_transaction(transaction)
    except ClientError as e:
        raise Exception('Error when adding transaction to DynamoDB', inner=e)
    return transaction

def update_user_watchlist(user, movie, ticket_id):
    try:
        watch_list = user.get('watch_list', [])
        
        watch_list_node = create_watchlist_node(movie, ticket_id)
        watch_list.append(watch_list_node)
        user['watch_list'] = watch_list
        print("user after updating watch list: ", user)
        dynamodb_utilities.update_user(user)
    except ClientError as e:
        raise Exception('Error when updating user watchlist', inner=e)
    return user

def update_movie_for_booking(movie, movie_id, ticket_booked, ticket_price, ticket_quantity):
    try:
        movie['total_sales'] = movie['total_sales'] + ticket_quantity
        movie['total_tickets_business'] = movie['total_tickets_business'] + ticket_price*ticket_quantity
        movie['ticket_booked'] = ticket_booked
        movie.pop('movie_name')
        dynamodb_utilities.update_movie(movie_id, movie)
    except ClientError as e:
        raise Exception('Error when updating movie for booking', inner=e)
    return movie
