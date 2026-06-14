import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PlayerProfile')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super().default(obj)

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']
    
    response = table.get_item(Key={'userId': user_id})
    item = response.get('Item')
    
    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Player not found'})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(item, cls=DecimalEncoder)
    }
