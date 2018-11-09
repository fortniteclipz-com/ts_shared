import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Recent
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_recents_name = f"{ts_config.get('dynamodb.tables.recents.name')}-{stage}"
table_recents = resource.Table(table_recents_name)

def save_montage(montage):
    recent_montage = get_montage()

    if montage.montage_id in recent_montage.media_ids:
        recent_montage.media_ids.remove(montage.montage_id)
    recent_montage.media_ids.insert(0, montage.montage_id)

    logger.info("save_montage | start", montage=montage, recent_montage=recent_montage)
    r = table_recents.put_item(
        Item=_replace_floats(recent_montage),
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("save_montage | success", response=r)

def get_montage():
    logger.info("get_montage | start")
    r = table_recents.get_item(
        Key={
            'media': 'montage',
        },
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_montage | success", response=r)

    if 'Item' in r:
        recent_montage = ts_model.Recent(**_replace_decimals(r['Item']))
    else:
        recent_montage = ts_model.Recent(
            media='montage',
            media_ids=[],
        )

    return recent_montage

def save_stream(stream):
    recent_stream = get_stream(stream)

    if stream.stream_id in recent_stream.media_ids:
        recent_stream.media_ids.remove(stream.stream_id)
    recent_stream.media_ids.insert(0, stream.stream_id)

    logger.info("save_stream | start", stream=stream, recent_stream=recent_stream)
    r = table_recents.put_item(
        Item=_replace_floats(recent_stream),
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("save_stream | success", response=r)

def get_stream():
    logger.info("get_stream | start")
    r = table_recents.get_item(
        Key={
            'media': 'stream',
        },
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_stream | success", response=r)

    if 'Item' in r:
        recent_stream = ts_model.Recent(**_replace_decimals(r['Item']))
    else:
        recent_stream = ts_model.Recent(
            media='stream',
            media_ids=[],
        )

    return recent_stream

