import json
from typing import Union
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class LambdaProxyResponse:

    def __init__(self, body: Union[str, dict], status_code: int, headers: dict = None, multi_value_headers: dict = None,
                 is_base64_encoded: bool = False, **kwargs):
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.multi_value_headers = multi_value_headers
        self.is_base64_encoded = is_base64_encoded

    def generate_response(self):
        # Adding CORS
        headers = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
        if self.headers:
            headers = {**headers, **self.headers}

        return {
            'statusCode': self.status_code,
            'body': self.body if isinstance(self.body, str) else json.dumps(self.body, cls=DecimalEncoder),
            'headers': headers,
            'multiValueHeaders': self.multi_value_headers,
            'isBase64Encoded': self.is_base64_encoded
        }


class SimpleResponse(LambdaProxyResponse):
    def __init__(self, body, status_code=200):
        super().__init__(body, status_code)
