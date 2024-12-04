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
            # check if tickets are booked for the movie
            movie = get_movie(movie_name)
            if movie['ticket_booked'] == True:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'message': 'Tickets are booked for the movie. Cannot delete the movie'
                    })
                }
            else:
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

    

