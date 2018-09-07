import ts_config
import ts_logger
import ts_model.StreamSegment
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_stream_segments_name = ts_config.get('aws.dynamodb.stream-segments.name')
table_stream_segments = resource.Table(table_stream_segments_name)

def save_stream_segment(stream_segment):
    logger.info("save_stream_segment | start", stream_segment=stream_segment)
    r = table_stream_segments.put_item(
        Item=_replace_floats(stream_segment),
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("save_stream_segment | success", response=r)

def get_stream_segment(stream_id, segment):
    logger.info("get_stream_segment | start", stream_id=stream_id, segment=segment)
    r = table_stream_segments.get_item(
        Key={
            'stream_id': stream_id,
            'segment': segment,
        },
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_stream_segment | success", response=r)
    if 'Item' not in r:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENT__NOT_EXIST)
    return ts_model.StreamSegment(**_replace_decimals(r['Item']))

def save_stream_segments(stream_segments):
    logger.info("save_stream_segments | start", stream_segments_length=len(stream_segments))
    with table_stream_segments.batch_writer() as batch:
        for ss in stream_segments:
            batch.put_item(
                Item=_replace_floats(ss),
            )
    logger.info("save_stream_segments | success")

def get_stream_segments(stream_id, exclusiveStartKey=None):
    logger.info("get_stream_segments | start", stream_id=stream_id)
    stream_segments = []

    if exclusiveStartKey is not None:
        exclusiveStartKey = {
            'ExclusiveStartKey': exclusiveStartKey,
        }
    else:
        exclusiveStartKey = {}

    r = table_stream_segments.query(
        KeyConditionExpression="stream_id = :stream_id",
        ExpressionAttributeValues=_replace_floats({
            ':stream_id': stream_id,
        }),
        **exclusiveStartKey,
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_stream_segments | success", response=r)
    if len(r['Items']) == 0:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENTS__NOT_EXIST)
    stream_segments += list(map(lambda ss: ts_model.StreamSegment(**ss), _replace_decimals(r['Items'])))

    lastEvaluatedKey = r.get('LastEvaluatedKey')
    if lastEvaluatedKey is not None:
        stream_segments += get_stream_segments(stream_id, lastEvaluatedKey)

    return stream_segments
