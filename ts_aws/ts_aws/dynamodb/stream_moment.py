import ts_config
import ts_logger
import ts_model.StreamMoment
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_stream_moments_name = f"{ts_config.get('dynamodb.tables.stream-moments.name')}-{stage}"
table_stream_moments = resource.Table(table_stream_moments_name)

def save_stream_moments(stream_moments):
    logger.info("save_stream_moments | start", stream_moments_length=len(stream_moments))
    with table_stream_moments.batch_writer() as batch:
        for sm in stream_moments:
            batch.put_item(
                Item=_replace_floats(sm),
            )
    logger.info("save_stream_moments | success")

def get_stream_moments(stream_id, exclusiveStartKey=None):
    logger.info("get_stream_moments | start", stream_id=stream_id)
    stream_moments = []

    if exclusiveStartKey is not None:
        exclusiveStartKey = {
            'ExclusiveStartKey': exclusiveStartKey,
        }
    else:
        exclusiveStartKey = {}

    r = table_stream_moments.query(
        IndexName='stream_id-time-index',
        KeyConditionExpression='stream_id = :stream_id',
        ExpressionAttributeValues=_replace_floats({
            ':stream_id': stream_id,
        }),
        **exclusiveStartKey,
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_stream_moments | success", response=r)
    if len(r['Items']) == 0:
        raise ts_model.Exception(ts_model.Exception.STREAM_MOMENTS__NOT_EXIST)
    stream_moments += list(map(lambda sm: ts_model.StreamMoment(**sm), _replace_decimals(r['Items'])))

    lastEvaluatedKey = r.get('LastEvaluatedKey')
    if lastEvaluatedKey is not None:
        stream_moments += get_stream_moments(stream_id, lastEvaluatedKey)

    return stream_moments
