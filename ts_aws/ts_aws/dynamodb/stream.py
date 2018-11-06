import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Stream
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import datetime

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_streams_name = f"{ts_config.get('dynamodb.tables.streams.name')}-{stage}"
table_streams = resource.Table(table_streams_name)

def save_stream(stream):
    logger.info("save_stream | start", stream=stream)
    stream._last_modified = datetime.datetime.utcnow().isoformat()
    r = table_streams.put_item(
        Item=_replace_floats(stream),
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("save_stream | success", response=r)

def get_stream(stream_id):
    logger.info("get_stream | start", stream_id=stream_id)
    r = table_streams.get_item(
        Key={
            'stream_id': stream_id
        },
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_stream | success", response=r)
    if 'Item' not in r:
        raise ts_model.Exception(ts_model.Exception.STREAM__NOT_EXIST)
    return ts_model.Stream(**_replace_decimals(r['Item']))

def get_all_streams(limit):
    logger.info("get_all_streams | start", limit=limit)
    r = table_streams.scan(
        Limit=limit,
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_all_streams | success", response=r)
    return list(map(lambda c: ts_model.Stream(**c), _replace_decimals(r['Items'])))
