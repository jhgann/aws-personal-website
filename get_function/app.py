import boto3
import os
from boto3.dynamodb.conditions import Key

tableName = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)

def lambda_handler(event, context):

    response = table.query(
        KeyConditionExpression=Key('ID').eq('visitors'))
    count = response['Items'][0]['visitors']
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Credentials': '*',
            'Content-Type': 'application/json'
        },
        'body': count
    }