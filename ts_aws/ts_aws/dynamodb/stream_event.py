import ts_config
import ts_logger
import ts_model.StreamEvent
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_stream_events_name = ts_config.get('aws.dynamodb.stream-events.name')
table_stream_events = resource.Table(table_stream_events_name)

def save_stream_events(stream_events):
    logger.info("save_stream_events | start", stream_events_length=len(stream_events))
    with table_stream_events.batch_writer() as batch:
        for ss in stream_events:
            batch.put_item(
                Item=_replace_floats(ss),
            )
    logger.info("save_stream_events | success")

def get_stream_events(stream_id, exclusiveStartKey=None):
    logger.info("get_stream_events | start", stream_id=stream_id)
    stream_segments = []

    if exclusiveStartKey is not None:
        exclusiveStartKey = {
            'ExclusiveStartKey': exclusiveStartKey,
        }
    else:
        exclusiveStartKey = {}

    r = table_stream_segments.query(
        IndexName="stream_id-time-index",
        KeyConditionExpression="stream_id = :stream_id",
        ExpressionAttributeValues=_replace_floats({
            ':stream_id': stream_id,
        }),
        **exclusiveStartKey,
        ReturnConsumedCapacity="TOTAL",
    )
    logger.info("get_stream_events | success", response=r)
    if len(r['Items']) == 0:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENTS__NOT_EXIST)
    stream_segments += list(map(lambda mc: ts_model.StreamEvent(**mc), _replace_decimals(r['Items'])))

    lastEvaluatedKey = r.get('LastEvaluatedKey')
    if lastEvaluatedKey is not None:
        stream_segments += get_stream_events(stream_id, lastEvaluatedKey)

    return stream_segments
