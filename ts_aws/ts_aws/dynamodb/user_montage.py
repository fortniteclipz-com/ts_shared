import ts_config
import ts_logger
import ts_model.UserMontage
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_user_montages_name = f"{ts_config.get('dynamodb.tables.user-montages.name')}-{stage}"
table_user_montages = resource.Table(table_user_montages_name)

def save_user_montage(user_montage):
    logger.info("save_user_montage | start", user_montage=user_montage)
    r = table_user_montages.put_item(
        Item=_replace_floats(user_montage),
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("save_user_montage | success", response=r)

def get_all_user_montages():
    logger.info("get_all_user_montages | start")
    r = table_user_montages.scan(
        IndexName='created-index',
        Limit=25,
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_all_user_montages | success", response=r)
    return list(map(lambda um: ts_model.UserMontage(**um), _replace_decimals(r['Items'])))

def get_user_montages(user_id):
    logger.info("get_user_montages | start", user_id=user_id)
    r = table_user_montages.query(
        IndexName='user_id-created-index',
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues=_replace_floats({
            ':user_id': user_id,
        }),
        ScanIndexForward=False,
        Limit=25,
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_user_montages | success", response=r)
    return list(map(lambda um: ts_model.UserMontage(**um), _replace_decimals(r['Items'])))
