import ts_config
import ts_logger
import ts_model.Clip
import ts_model.ClipSegment
import ts_model.Exception
import ts_model.StreamSegment
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import traceback

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_clips_name = ts_config.get('aws.dynamodb.clips.name')
table_clips = resource.Table(table_clips_name)
table_stream_segments_name = ts_config.get('aws.dynamodb.stream-segments.name')
table_stream_segments = resource.Table(table_stream_segments_name)
table_clip_segments_name = ts_config.get('aws.dynamodb.clip-segments.name')
table_clip_segments = resource.Table(table_clip_segments_name)

def save_clip(clip):
    logger.info("save_clip | start", clip=clip)
    r = table_clips.put_item(
        Item=_replace_floats(clip),
        ReturnConsumedCapacity="TOTAL"
    )
    logger.info("save_clip | success", response=r)

def get_clip(clip_id):
    logger.info("get_clip | start", clip_id=clip_id)
    r = table_clips.get_item(
        Key={
            'clip_id': clip_id
        },
        ReturnConsumedCapacity="TOTAL"
    )
    logger.info("get_clip | success", response=r)
    if 'Item' not in r:
        raise ts_model.Exception(ts_model.Exception.CLIP__NOT_EXIST)
    return ts_model.Clip(**_replace_decimals(r['Item']))

def get_clips(clip_ids):
    logger.info("get_clips | start", clip_ids=clip_ids)
    r = resource.batch_get_item(
        RequestItems={
            table_clips_name: {
                'Keys': list(map(lambda c_id: {'clip_id': c_id}, clip_ids))
            }
        },
        ReturnConsumedCapacity="TOTAL"
    )
    logger.info("get_clips | success", response=r)
    if len(r['Responses'][table_clips_name]) == 0:
            raise ts_model.Exception(ts_model.Exception.CLIPS__NOT_EXIST)
    return list(map(lambda cs: ts_model.Clip(**cs), _replace_decimals(r['Responses'][table_clips_name])))

def get_all_clips(limit):
    logger.info("get_all_clips | start", limit=limit)
    r = table_clips.scan(
        Limit=limit,
        ReturnConsumedCapacity="TOTAL"
    )
    logger.info("get_all_clips | success", response=r)
    return list(map(lambda c: ts_model.Clip(**c), _replace_decimals(r['Items'])))

def get_clip_stream_segments(stream, clip):
    logger.info("get_clip_stream_segments | start uno", stream=stream, clip=clip)
    r = table_stream_segments.query(
        IndexName="stream_id-time_in-index",
        KeyConditionExpression="stream_id = :stream_id AND time_in <= :time_in",
        ExpressionAttributeValues=_replace_floats({
            ':stream_id': clip.stream_id,
            ':time_in': clip.time_in,
        }),
        ScanIndexForward=False,
        Limit=2,
        ReturnConsumedCapacity="TOTAL"
    )
    logger.info("get_clip_stream_segments | success uno", response=r)

    if len(r['Items']) == 2:
        last_css = ts_model.StreamSegment(**_replace_decimals(r['Items'][1]))
        exclusiveStartKey = {
            'ExclusiveStartKey': _replace_floats({
                'stream_id': last_css.stream_id,
                'time_in': last_css.time_in,
                'segment': last_css.segment,
            })
        }
    else:
        exclusiveStartKey = {}

    logger.info("get_clip_stream_segments | start duo", stream=stream, clip=clip, exclusiveStartKey=exclusiveStartKey)
    r = table_stream_segments.query(
        IndexName="stream_id-time_in-index",
        KeyConditionExpression="stream_id = :stream_id AND time_in < :time_out",
        ExpressionAttributeValues=_replace_floats({
            ':stream_id': clip.stream_id,
            ':time_out': clip.time_out,
        }),
        ReturnConsumedCapacity="TOTAL",
        **exclusiveStartKey
    )
    logger.info("get_clip_stream_segments | success duo", response=r)

    if len(r['Items']) == 0:
        raise ts_model.Exception(ts_model.Exception.CLIP_SEGMENTS__NOT_EXIST)
    return list(map(lambda ss: ts_model.StreamSegment(**ss), _replace_decimals(r['Items'])))
