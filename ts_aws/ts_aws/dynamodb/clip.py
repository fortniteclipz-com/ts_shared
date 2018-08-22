import ts_aws.dynamodb.stream_segment
import ts_config
import ts_logger
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import enum

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_clips_name = ts_config.get('aws.dynamodb.clips.name')
table_clips = resource.Table(table_clips_name)
table_stream_segments_name = ts_config.get('aws.dynamodb.stream-segments.name')
table_stream_segments = resource.Table(table_stream_segments_name)

class Clip():
    def __init__(self, **kwargs):
        self.clip_id = kwargs.get('clip_id')
        self.stream_id = kwargs.get('stream_id')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')

        self.key_playlist_audio = kwargs.get('key_playlist_audio')
        self.key_playlist_master = kwargs.get('key_playlist_master')
        self.key_playlist_video = kwargs.get('key_playlist_video')

        self._status = kwargs.get('_status')

class ClipStatus(enum.IntEnum):
    INITIALIZING = 0
    READY = 1
    def __repr__(self):
        return self.name

def save_clip(clip):
    try:
        r = table_clips.put_item(
            Item=_replace_floats(clip.__dict__),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("save_clip", response=r)
    except Exception as e:
        logger.warn("save_clip error", error=e)

def get_clip(clip_id):
    try:
        r = table_clips.get_item(
            Key={
                'clip_id': clip_id
            },
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_clip", response=r)
        return Clip(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.warn("get_clip error", error=e)
        return None

def get_clips(clip_ids):
    try:
        r = resource.batch_get_item(
            RequestItems={
                table_clips_name: {
                    'Keys': list(map(lambda c_id: {'clip_id': c_id}, clip_ids))
                }
            },
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_clips", response=r)
        return list(map(lambda cs: Clip(**cs), _replace_decimals(r['Responses'][table_clips_name])))
    except Exception as e:
        logger.warn("get_clips error", error=e)
        return []

def get_all_clips():
    try:
        r = table_clips.scan(
            Limit=23,
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_all_clips", response=r)
        return list(map(lambda c: Clip(**c), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_all_clips error", error=e)
        return []

def get_clip_stream_segments(stream, clip):
    try:
        r = table_stream_segments.query(
            IndexName="stream_id-time_in-index",
            KeyConditionExpression="stream_id = :stream_id AND time_in <= :time_in",
            ExpressionAttributeValues=_replace_floats({
                ':stream_id': clip.stream_id,
                ':time_in': clip.time_in + stream.time_offset,
            }),
            ScanIndexForward=False,
            Limit=2,
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_clip_stream_segments | first", response=r)

        if len(r['Items']) == 2:
            last_css = ts_aws.dynamodb.stream_segment.StreamSegment(**_replace_decimals(r['Items'][1]))
            exclusiveStartKey = {
                'ExclusiveStartKey': _replace_floats({
                    'stream_id': last_css.stream_id,
                    'time_in': last_css.time_in,
                    'segment': last_css.segment,
                })
            }
        else:
            exclusiveStartKey = {}

        r = table_stream_segments.query(
            IndexName="stream_id-time_in-index",
            KeyConditionExpression="stream_id = :stream_id AND time_in < :time_out",
            ExpressionAttributeValues=_replace_floats({
                ':stream_id': clip.stream_id,
                ':time_out': clip.time_out + stream.time_offset,
            }),
            ReturnConsumedCapacity="TOTAL",
            **exclusiveStartKey
        )
        logger.info("get_clip_stream_segments | final", response=r)
        return list(map(lambda ss: ts_aws.dynamodb.stream_segment.StreamSegment(**ss), _replace_decimals(r['Items'])))

    except Exception as e:
        logger.warn("get_clip_stream_segments error", error=e)
        return []
