# dynamodb operation to read user data and compare username and password with input
def sign_in_user(user_id:str, password:str):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')

    try:
        response = table.get_item(Key={'user_id': user_id})
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise Exception('Error fetching user data')

    if 'Item' not in response:
        raise Exception('User does not exist')

    user = response['Item']
    if user['password'] != password:
        raise Exception('Incorrect password')

    return 'User signed in successfully'