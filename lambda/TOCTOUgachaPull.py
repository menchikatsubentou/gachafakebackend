import json
import boto3
import random
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PlayerProfile')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super().default(obj)

GACHA_ITEMS = ['sword', 'shield', 'potion', 'bow', 'staff']
GACHA_COST = 10

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']

    response = table.get_item(Key={'userId': user_id})
    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Player not found'})
        }

    current_gems = int(item['gems'])
    if current_gems < GACHA_COST:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Not enough gems'})
        }

    pulled_item = random.choice(GACHA_ITEMS)

    try:
        table.update_item(
            Key={'userId': user_id},
            UpdateExpression='SET gems = gems - :cost, inventory = list_append(inventory, :item)',
            ConditionExpression='gems >= :cost', 
            ExpressionAttributeValues={
                ':cost': Decimal(GACHA_COST),
                ':item': [pulled_item]
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Not enough gems'})
            }
        raise

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Gacha pull successful',
            'item_received': pulled_item,
            'gems_remaining': current_gems - GACHA_COST
        }, cls=DecimalEncoder)
    }
