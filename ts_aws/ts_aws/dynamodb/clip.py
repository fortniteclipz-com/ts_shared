import ts_config
import ts_logger

from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import shortuuid

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_clips_name = ts_config.get('aws.dynamodb.clips.name')
table_clip_segments_name = ts_config.get('aws.dynamodb.clip-segments.name')
table_clips = resource.Table(table_clips_name)
table_clip_segments = resource.Table(table_clip_segments_name)

class Clip():
    def __init__(self, **kwargs):
        self.clip_id = kwargs.get('clip_id')
        self.stream_id = kwargs.get('stream_id')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')

        self.key_playlist_audio = kwargs.get('key_playlist_audio')
        self.key_playlist_master = kwargs.get('key_playlist_master')
        self.key_playlist_video = kwargs.get('key_playlist_video')

    def is_init(self):
        init_keys = [
            'key_playlist_audio',
            'key_playlist_master',
            'key_playlist_video',
        ]
        return all(ik in self.__dict__ and self.__dict__[ik] is not None for ik in init_keys)

class ClipSegment():
    def __init__(self, **kwargs):
        self.clip_id = kwargs.get('clip_id')
        self.segment = kwargs.get('segment')

        self.audio_packets_byterange = kwargs.get('audio_packets_byterange')
        self.audio_packets_pos = kwargs.get('audio_packets_pos')
        self.audio_time_duration = kwargs.get('audio_time_duration')
        self.audio_time_out = kwargs.get('audio_time_out')
        self.audio_time_in = kwargs.get('audio_time_in')
        self.audio_url_media = kwargs.get('audio_url_media')
        self.video_packets_byterange = kwargs.get('video_packets_byterange')
        self.video_packets_pos = kwargs.get('video_packets_pos')
        self.video_time_duration = kwargs.get('video_time_duration')
        self.video_time_out = kwargs.get('video_time_out')
        self.video_time_in = kwargs.get('video_time_in')
        self.video_url_media = kwargs.get('video_url_media')

        self.discontinuity = kwargs.get('discontinuity')

    def is_init(self):
        init_keys = [
            'audio_time_duration',
            'audio_time_out',
            'audio_time_in',
            'audio_url_media',
            'video_time_duration',
            'video_time_out',
            'video_time_in',
            'video_url_media',
        ]
        return all(ik in self.__dict__ and self.__dict__[ik] is not None for ik in init_keys)

def save_clip(clip):
    if not clip.clip_id:
        clip.clip_id = f"c-{shortuuid.uuid()}"
    table_clips.put_item(Item=_replace_floats(clip.__dict__))
    _replace_decimals(clip.__dict__)
    return clip

def get_clip(clip_id):
    try:
        response = table_clips.get_item(Key={'clip_id': clip_id})
        return Clip(**_replace_decimals(response['Item']))
    except Exception as e:
        logger.warn("get_clip error", error=e)
        return None

def get_clips(clip_ids):
    try:
        response = resource.batch_get_item(
            RequestItems={
                'ts-clips': {
                    'Keys': list(map(lambda c_id: {'clip_id': c_id}, clip_ids))
                }
            }
        )
        return list(map(lambda cs: Clip(**cs), _replace_decimals(response['Responses']['ts-clips'])))
    except Exception as e:
        logger.warn("get_clips error", error=e)
        return []

# TODO: limit and sort
def get_all_clips():
    try:
        response = table_clips.scan()
        return list(map(lambda c: Clip(**c), _replace_decimals(response['Items'])))
    except Exception as e:
        logger.warn("get_all_clips error", error=e)
        return []

def save_clip_segments(clip_segments):
    with table_clip_segments.batch_writer() as batch:
        for cs in clip_segments:
            batch.put_item(Item=_replace_floats(cs.__dict__))
    return list(map(lambda cs: ClipSegment(**_replace_decimals(cs.__dict__)), clip_segments))

# TODO: new syntax
def get_clip_segments(clip_id):
    try:
        response = table_clip_segments.query(
            KeyConditions={
                'clip_id': {
                    'AttributeValueList': [clip_id],
                    'ComparisonOperator': 'EQ',
                }
            }
        )
        return list(map(lambda cs: ClipSegment(**cs), _replace_decimals(response['Items'])))
    except Exception as e:
        logger.warn("get_clip_segments error", error=e)
        return []

# TODO: batch get
def get_clips_segments(clip_ids):
    try:
        response = table_clip_segments.scan(
            ScanFilter={
                'clip_id': {
                    'AttributeValueList': clip_ids,
                    'ComparisonOperator': 'IN',
                }
            }
        )
        return list(map(lambda cs: ClipSegment(**cs), _replace_decimals(response['Items'])))
    except Exception as e:
        logger.warn("get_clips_segments error", error=e)
        return []
