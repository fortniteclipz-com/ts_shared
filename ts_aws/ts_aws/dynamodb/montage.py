import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Montage
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_montages_name = ts_config.get('aws.dynamodb.tables.montages.name')
table_montages = resource.Table(table_montages_name)

def save_montage(montage):
    logger.info("save_montage | start", montage=montage)
    r = table_montages.put_item(
        Item=_replace_floats(montage),
        ReturnConsumedCapacity="TOTAL",
    )
    _replace_decimals(montage)
    logger.info("save_montage | success", response=r)

def get_montage(montage_id):
    logger.info("get_montage | start", montage_id=montage_id)
    r = table_montages.get_item(
        Key={'montage_id': montage_id},
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_montage | success", response=r)
    if 'Item' not in r:
        raise ts_model.Exception(ts_model.Exception.MONTAGE__NOT_EXIST)
    return ts_model.Montage(**_replace_decimals(r['Item']))

def get_all_montages(limit):
    logger.info("get_all_montages | start", limit=limit)
    r = table_montages.scan(
        Limit=limit,
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_all_montages | success", response=r)
    return list(map(lambda c: ts_model.Montage(**c), _replace_decimals(r['Items'])))
