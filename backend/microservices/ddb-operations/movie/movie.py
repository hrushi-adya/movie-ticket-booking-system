import json
import logging
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from json import JSONDecodeError

from util.dynamodb_utilities import delete_movie, get_movies
from util.utilities import decimal_to_native

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
            movies = get_movies()
            movies = decimal_to_native(movies)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'movies': movies # Include the original input map and new ticket_id
                    # 'email_response': response
                })
            }   
        elif http_method == "PUT":
            print("Updating Movies")
        elif http_method == "DELETE":
            movie_id = event['queryStringParameters']['movie_id']
            response = delete_movie(movie_id)
            if response:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Movie deleted successfully'
                    })
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'message': 'Error deleting movie'
                    })
                }

    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except Exception as e:
        raise Exception('Error when performing GET API', e)

    # movie dictionary 
    # movie_name = body["movie_name"]
    # movie_description = body["movie_description"]
    # genre = body["genre"]
    # movie_director = body["movie_director"]
    # release_date = body["release_date"]
    # ticket_price = body["ticket_price"]
    # movie_length = body["movie_length"]
    # movie_thumbnail = body["movie_thumbnail"]
    # movie_available = body["movie_available"]

    # movie = {}
    # movie['movie_id'] = movie_id
    # movie['movie_name'] = movie_name
    # movie['movie_description'] = movie_description
    # movie['genre'] = genre
    # movie['movie_director'] = movie_director
    # movie['release_date'] = release_date
    # movie['ticket_price'] = ticket_price
    # movie['movie_length'] = movie_length
    # movie['movie_thumbnail'] = movie_thumbnail
    # movie['movie_available'] = movie_available

   
    # movie = update_movie(movie_id, movie)

    return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Ticket booked successfully',
                'data1': json.dumps(movies) # Include the original input map and new ticket_id
                # 'email_response': response
            })
    }

def update_movie(movie_id, movie_details):
    # Initialize a session using Amazon DynamoDB
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY',
        aws_secret_access_key='YOUR_SECRET_KEY',
        region_name='YOUR_REGION'
    )

    # Initialize DynamoDB resource
    dynamodb = session.resource('dynamodb')

    # Select your DynamoDB table
    table = dynamodb.Table()

    try:
        # Put item into the table
        response = table.put_item(
            Item={
                'movie_id': movie_id,
                **movie_details
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

