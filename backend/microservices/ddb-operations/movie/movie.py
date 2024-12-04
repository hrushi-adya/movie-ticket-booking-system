import json
import logging
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from json import JSONDecodeError

from util.dynamodb_utilities import delete_movie, get_movie, get_movies, update_movie
from util.utilities import decimal_to_native, filter_params, update_dictionary

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
                movie_name = event['queryStringParameters']['movie_name']
                print("movie name: ", movie_name)
                movies = get_movie(movie_name)
                movies = decimal_to_native(movies)
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'movies': movies # Include the original input map and new ticket_id
                        # 'email_response': response
                    })
                }
            else:
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
            body = json.loads(event['body'])
            movie_name = event['queryStringParameters']['movie_name']
            filtered_movie = filter_params(body)
            filtered_movie = update_dictionary(get_movie(movie_name), filtered_movie)
            response = update_movie(movie_name, filtered_movie)
            return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'movies': response
                    })
            }
        elif http_method == "DELETE":
            movie_name = event['queryStringParameters']['movie_name']
            print("movie name: ", movie_name)
            response = delete_movie(movie_name)
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
    
    movie = {}
    movie['movie_name'] = movie_name
    movie['movie_description'] = movie_description
    movie['genre'] = genre
    movie['movie_director'] = movie_director
    movie['release_date'] = release_date
    movie['ticket_price'] = ticket_price
    movie['movie_length'] = movie_length
    movie['movie_available'] = movie_available
    movie['movie_showtimes'] = movie_showtimes
    
    # movie = update_movie(movie_id, movie)

    return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Ticket booked successfully',
                'data1': json.dumps(movies) # Include the original input map and new ticket_id
                # 'email_response': response
            })
    }

# def update_movie(movie_id, movie_details):
#     # Initialize a session using Amazon DynamoDB
#     session = boto3.Session(
#         aws_access_key_id='YOUR_ACCESS_KEY',
#         aws_secret_access_key='YOUR_SECRET_KEY',
#         region_name='YOUR_REGION'
#     )

#     # Initialize DynamoDB resource
#     dynamodb = session.resource('dynamodb')

#     # Select your DynamoDB table
#     table = dynamodb.Table()

#     try:
#         # Put item into the table
#         response = table.put_item(
#             Item={
#                 'movie_id': movie_id,
#                 **movie_details
#             }
#         )
#         return response
#     except ClientError as e:
#         print(e.response['Error']['Message'])
#         return None

