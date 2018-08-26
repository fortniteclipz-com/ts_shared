import ts_config
import ts_logger
import ts_model.Montage
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import traceback

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_montages_name = ts_config.get('aws.dynamodb.montages.name')
table_montages = resource.Table(table_montages_name)

def save_montage(montage):
    try:
        logger.info("save_montage | start", montage=montage.__dict__    )
        r = table_montages.put_item(
            Item=_replace_floats(montage.__dict__),
            ReturnConsumedCapacity="TOTAL"
        )
        _replace_decimals(montage.__dict__)
        logger.info("save_montage | success", response=r)
    except Exception as e:
        logger.error("save_montage | error", traceback=''.join(traceback.format_tb(e.__traceback__)))

def get_montage(montage_id):
    try:
        logger.info("get_montage | start", montage_id=montage_id)
        r = table_montages.get_item(
            Key={'montage_id': montage_id},
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_montage | success", response=r)
        return ts_model.Montage(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.error("get_montage | error", traceback=''.join(traceback.format_tb(e.__traceback__)))
        return None

def get_all_montages():
    try:
        logger.info("get_all_montages | start")
        r = table_montages.scan(
            Limit=23,
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_all_montages | success", response=r)
        return list(map(lambda c: ts_model.Montage(**c), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.error("get_all_montages | error", traceback=''.join(traceback.format_tb(e.__traceback__)))
        return []
