import boto3

def add_movie_thumbnail(movie_thumbnail):
    s3 = boto3.client('s3')
    bucket_name = 'movie-thumbnail-bucket'
    s3.put_object(Bucket=bucket_name, Key=movie_thumbnail)

    return movie_thumbnail

# Method to get object from S3 bucket
def get_movie_thumbnail(movie_thumbnail):
    s3 = boto3.client('s3')
    bucket_name = 'movie-thumbnail-bucket'
    response = s3.get_object(Bucket=bucket_name, Key=movie_thumbnail)

    return response
