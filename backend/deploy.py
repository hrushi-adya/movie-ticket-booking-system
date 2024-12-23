import re
import os
from uuid import uuid4
from zipfile import ZipFile
import boto3
import botocore.exceptions
import json
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

LOCAL_FILENAME = str(uuid4())
PATTERNS = [
    'microservice',
    'model',
    # 'schemas',
    'util',
    'cognito',
    # 'location'
]

CWD = os.getcwd()
if os.path.exists(LOCAL_FILENAME):
    os.remove(LOCAL_FILENAME)

with ZipFile(LOCAL_FILENAME, 'a') as zipObj:
    for root, dirs, files in os.walk(CWD):
        for file in files:
            abs_path = root + os.sep + file
            rel_path = abs_path[len(CWD) + 1:]
            #print(rel_path)
            for pattern in PATTERNS:
                if rel_path.__contains__(pattern) and not rel_path.__contains__('venv') and not rel_path.__contains__('python'):
                    zipObj.write(rel_path, rel_path)
                    print(rel_path+'--ui')
                    break

if not os.path.exists(LOCAL_FILENAME):
    raise RuntimeError('Unable to zip')

# Updating phase
with open('conf/deploy_config.json') as f:
    config = json.load(f)


def parse_s3_url(s3url):
    parsed_url = urlparse(s3url)
    if not parsed_url.netloc:
        raise RuntimeError(
            'Please provide a bucket_name instead of "%s"' % s3url)
    else:
        bucket_name = parsed_url.netloc
        key = parsed_url.path.strip('/')
        return bucket_name, key


# Upload to S3
s3_client = boto3.client('s3',aws_access_key_id='',
                         aws_secret_access_key='',
                         region_name='')
[bucket, key] = parse_s3_url(config['artifact'])
s3_upload_res = s3_client.upload_file(LOCAL_FILENAME, bucket, key, ExtraArgs={
    'ServerSideEncryption': "AES256"
})
print('S3 Uploaded')
#os.remove(LOCAL_FILENAME)

# Update Lambda functions
lambda_functions = config.get('lambda_functions', [])
if not lambda_functions:
    print('No Lambda Functions defined')

lambda_default_conf = json.dumps(config.get('lambda_function_default'))
lambda_client = boto3.client('lambda', aws_access_key_id='',
                             aws_secret_access_key='',
                             region_name='')


def update_lambda_function_task(func, lambda_client):
    func_config = json.loads(lambda_default_conf)
    func_config.update(func)

    if 'FunctionName' not in func_config:
        raise RuntimeError('No FunctionName in a lambda function')

    func_name = func["FunctionName"]
    print(f' Processing: {func_name}')
    print(f' Processing: {func_config}')
    get_function_res = None
    try:
        get_function_res = lambda_client.get_function(FunctionName=func_config['FunctionName'])
        print(f'[{func_name}] (GET_FUNCTION) {str(get_function_res)}')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f'[{func_name}] (GET_FUNCTION) No function, create one')

    if get_function_res:

        config_updated = False
        while not config_updated:
            try:
                update_config_res = lambda_client.update_function_configuration(**func_config)
                print(f'[{func_name}] (UPDATE_FUNCTION_CONFIG) {str(update_config_res)}')
                config_updated = True
            except Exception as e:
                print(e)
                traceback.print_exc()
                raise e
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'ResourceConflictException':
                    print(f'[{func_name}] (UPDATE_FUNCTION_CONFIG) Function is being updated, retry in 3 sec...')
                    time.sleep(3)
                else:
                    raise e

        code_updated = False
        while not code_updated:
            try:
                print(f'[{func_name}] Is running')
                update_code_res = lambda_client.update_function_code(
                    FunctionName=func_config['FunctionName'],
                    S3Bucket=bucket,
                    S3Key=key,
                    Publish=True
                )
                print(f'[{func_name}] (UPDATE_FUNCTION_CODE) {str(update_code_res)}')
                code_updated = True
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'ResourceConflictException':
                    print(f'[{func_name}] (UPDATE_FUNCTION_CODE) Function is being updated, retry in 3 sec...')
                    time.sleep(3)
                else:
                    raise e
    else:
        func_config.update({
            'Code': {
                'S3Bucket': bucket,
                'S3Key': key
            },
        })
        create_function_res = lambda_client.create_function(**func_config)
        print(f'[{func_name}] (CREATE_FUNCTION) {str(create_function_res)}')


with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {}
    for func in lambda_functions:
        futures[executor.submit(update_lambda_function_task, func, lambda_client)] = func

    for f in as_completed(futures):
        print(f'{futures[f]["FunctionName"]} finished!')

print(f'All tasks finished!!!')
