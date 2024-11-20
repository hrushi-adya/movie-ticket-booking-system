import json
import logging
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
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
        elif http_method == 'GET':
            body = json.loads(event['body'])
            if body.get('movie_id') is not None:
                movie_id = body['movie_id']
                movie = get_movie(movie_id)
                return movie
    except JSONDecodeError as e:
        raise JSONDecodeError('Error when decoding json body', inner=e)
    except TypeError as e:
        raise TypeError('Error when decoding json body', inner=e)

    # movie dictionary 
    movie_id = uuid4().hex
    movie_name = body["movie_name"]
    movie_description = body["movie_description"]
    genre = body["genre"]
    movie_director = body["movie_director"]
    release_date = body["release_date"]
    ticket_price = body["ticket_price"]
    movie_length = body["movie_length"]
    movie_thumbnail = body["movie_thumbnail"]
    movie_available = body["movie_available"]

    movie = {}
    movie['movie_id'] = movie_id
    movie['movie_name'] = movie_name
    movie['movie_description'] = movie_description
    movie['genre'] = genre
    movie['movie_director'] = movie_director
    movie['release_date'] = release_date
    movie['ticket_price'] = ticket_price
    movie['movie_length'] = movie_length
    movie['movie_thumbnail'] = movie_thumbnail
    movie['movie_available'] = movie_available

   
    movie = update_movie(movie_id, movie)

    return SimpleResponse({
        'success': 200
    })

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
    table = dynamodb.Table(table_name)

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

