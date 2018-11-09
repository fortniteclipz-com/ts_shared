import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Montage
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_montages_name = f"{ts_config.get('dynamodb.tables.montages.name')}-{stage}"
table_montages = resource.Table(table_montages_name)

def save_montage(montage):
    logger.info("save_montage | start", montage=montage)
    r = table_montages.put_item(
        Item=_replace_floats(montage),
        ReturnConsumedCapacity='TOTAL',
    )
    _replace_decimals(montage)
    logger.info("save_montage | success", response=r)

def get_montage(montage_id):
    logger.info("get_montage | start", montage_id=montage_id)
    r = table_montages.get_item(
        Key={
            'montage_id': montage_id,
        },
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_montage | success", response=r)
    if 'Item' not in r:
        raise ts_model.Exception(ts_model.Exception.MONTAGE__NOT_EXIST)
    return ts_model.Montage(**_replace_decimals(r['Item']))

def get_montages(montage_ids):
    logger.info("get_montages | start", montage_ids=montage_ids)
    r = resource.batch_get_item(
        RequestItems={
            table_montages_name: {
                'Keys': list(map(lambda m_id: {'montage_id': m_id}, montage_ids)),
            }
        },
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_montages | success", response=r)
    if len(r['Responses'][table_montages_name]) == 0:
            raise ts_model.Exception(ts_model.Exception.MONTAGES__NOT_EXIST)
    return list(map(lambda m: ts_model.Montage(**m), _replace_decimals(r['Responses'][table_montages_name])))

def get_user_montages():
    pass
