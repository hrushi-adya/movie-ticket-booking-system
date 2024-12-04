import json
import logging
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
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
    http_method = event['httpMethod']

    try:
        if http_method == 'POST':        
            body = json.loads(event['body'])
    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except TypeError as e:
        raise TypeError('Error when decoding json body', inner=e)

    # movie dictionary 
    # movie_id = uuid4().hex
    movie_name = body["movie_name"]
    movie_description = body["movie_description"]
    genre = body["genre"]
    movie_director = body["movie_director"]
    release_date = body["release_date"]
    ticket_price = body["ticket_price"]
    movie_length = body["movie_length"]
    movie_available = body["movie_available"]
    movie_showtimes = body["movie_showtimes"]

    movie = add_movie(movie_name, movie_description, genre, movie_director, 
                      release_date, ticket_price, movie_length, movie_available, movie_showtimes)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Movie Added successfully',
            'data1': movie
            # 'email_response': response
        })
    }
def add_movie(movie_name, movie_description, genre, movie_director, 
              release_date, ticket_price, movie_length, movie_available, movie_showtimes):
    movie = {}
    # movie['movie_id'] = movie_id
    movie['movie_name'] = movie_name
    movie['movie_description'] = movie_description
    movie['genre'] = genre
    movie['movie_director'] = movie_director
    movie['release_date'] = release_date
    movie['ticket_price'] = ticket_price
    movie['movie_length'] = movie_length
    movie['movie_available'] = movie_available
    movie['movie_showtimes'] = movie_showtimes
    movie['movie_thumbnail'] = f"https://via.placeholder.com/300x200?text={movie_name}"
    movie['total_sales'] = 0
    
    try:
        movie = dynamodb_utilities.put_movie(movie)
    except ClientError as err:
        error_message = err.response['Error']['Message']
        logger.info(err.response['Error']['Message'])
        raise Exception(error_message)
    
    return movie

# Add S3 Put Object method to upload movie thumbnail to S3 bucket
def add_movie_thumbnail(movie_thumbnail):
    s3 = boto3.client('s3')
    bucket_name = 'movie-thumbnail-bucket'
    s3.put_object(Bucket=bucket_name, Key=movie_thumbnail)

    return movie_thumbnail

# Add SNS Publish method to send notification to all users for new movie release
