import boto3
from flask import Blueprint
import json

lam = Blueprint('lam', __name__)




@lam.route('/trigger')
def trigger_lambda():
    payload = json.dumps({"username": "Wu", "email": "wuw1998@gmail.com", "link": "this is a link"})
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='test-function',
                        InvocationType='RequestResponse',
                        Payload=payload)
    print(response)
    payload = response["Payload"].read()
    print(payload.decode("utf-8"))
    return payload.decode("utf-8")
