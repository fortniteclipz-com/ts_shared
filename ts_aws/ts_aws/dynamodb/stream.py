import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Stream
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import traceback

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_streams_name = ts_config.get('aws.dynamodb.streams.name')
table_streams = resource.Table(table_streams_name)

def save_stream(stream):
    logger.info("save_stream | start", stream=stream)
    try:
        r = table_streams.put_item(
            Item=_replace_floats(stream),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("save_stream | success", response=r)
    except Exception as e:
        logger.error("save_stream | error", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))

def get_stream(stream_id):
    logger.info("get_stream | start", stream_id=stream_id)
    try:
        r = table_streams.get_item(
            Key={
                'stream_id': stream_id
            },
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_stream | success", response=r)
        if 'Item' not in r:
            raise ts_model.Exception(ts_model.Exception.STREAM__NOT_EXIST)
        return ts_model.Stream(**_replace_decimals(r['Item']))
    except ts_model.Exception as e:
        logger.warn("get_stream | warn", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))
        return None
    except Exception as e:
        logger.error("get_stream | error", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))
        return None
