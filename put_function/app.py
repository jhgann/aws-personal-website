import simplejson as json
import boto3
import os
from botocore.exceptions import ClientError

tableName = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)

def respond(err, res=None):
    return {
        'statusCode': '500' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    try:
        response = table.update_item(     
            Key={'Id': 'visitcount'},   
            UpdateExpression='ADD ' + 'visitcount' + ' :incr',
            ExpressionAttributeValues={':incr': 1},    
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as err:
        return {
            'statusCode': '500',
            'body': err.response,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Credentials': '*',
            },
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "result": response['Attributes']
            })
        }
