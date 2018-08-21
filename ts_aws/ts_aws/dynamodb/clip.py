import ts_config
import ts_logger

from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_clips_name = ts_config.get('aws.dynamodb.clips.name')
table_clips = resource.Table(table_clips_name)

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

# good
def save_clip(clip):
    try:
        table_clips.put_item(
            Item=_replace_floats(clip.__dict__),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("save_clip", response=r)
    except Exception as e:
        logger.warn("save_clip error", error=e)

# good
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

# good
def get_clips(clip_ids):
    try:
        r = resource.batch_get_item(
            RequestItems={
                'ts-clips': {
                    'Keys': list(map(lambda c_id: {'clip_id': c_id}, clip_ids))
                }
            }
        )
        logger.info("get_clips", response=r)
        return list(map(lambda cs: Clip(**cs), _replace_decimals(r['Responses']['ts-clips'])))
    except Exception as e:
        logger.warn("get_clips error", error=e)
        return []

# TODO: limit and sort
def get_all_clips():
    try:
        r = table_clips.scan()
        return list(map(lambda c: Clip(**c), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_all_clips error", error=e)
        return []
