import ts_config
import ts_logger
import ts_model.StreamSegment
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import traceback

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_stream_segments_name = ts_config.get('aws.dynamodb.stream-segments.name')
table_stream_segments = resource.Table(table_stream_segments_name)

def save_stream_segment(stream_segment):
    logger.info("save_stream_segment | start", stream_segment=stream_segment)
    try:
        r = table_stream_segments.put_item(
            Item=_replace_floats(stream_segment),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("save_stream_segment | success", response=r)
    except Exception as e:
            logger.error("save_stream_segment | error", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))

def get_stream_segment(stream_id, segment):
    logger.info("get_stream_segment | start", stream_id=stream_id, segment=segment)
    try:
        r = table_stream_segments.get_item(
            Key={
                'stream_id': stream_id,
                'segment': segment,
            },
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_stream_segment | success", response=r)
        return ts_model.StreamSegment(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.error("get_stream_segment | error", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))
        return None

def save_stream_segments(stream_segments):
    logger.info("save_stream_segments | start", stream_segments_length=len(stream_segments))
    try:
        with table_stream_segments.batch_writer() as batch:
            for i, ss in enumerate(stream_segments):
                batch.put_item(
                    Item=_replace_floats(ss)
                )
        logger.info("save_stream_segments | success")
    except Exception as e:
        logger.error("save_stream_segments | error", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))

def get_stream_segments(stream_id):
    logger.info("get_stream_segments | start", stream_id=stream_id)
    try:
        r = table_stream_segments.query(
            KeyConditionExpression="stream_id = :stream_id",
            ExpressionAttributeValues=_replace_floats({
                ':stream_id': stream_id,
            }),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_stream_segments | success", response=r)
        return list(map(lambda ss: ts_model.StreamSegment(**ss), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.error("get_stream_segments | error", _module=f"{e.__class__.__module__}", _class=f"{e.__class__.__name__}", _message=str(e), traceback=''.join(traceback.format_exc()))
        return []
