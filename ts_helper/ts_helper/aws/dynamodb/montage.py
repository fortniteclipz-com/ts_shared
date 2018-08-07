import ts_config
import ts_logger
from ts_helper.aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import shortuuid

logger = ts_logger.get(__name__)
resource = boto3.resource('dynamodb')
table_montages_name = ts_config.get('aws.dynamodb.montages.name')
table_montage_clips_name = ts_config.get('aws.dynamodb.montage-clips.name')
table_montages = resource.Table(table_montages_name)
table_montage_clips = resource.Table(table_montage_clips_name)

class Montage():
    def __init__(self, **kwargs):
        self.montage_id = kwargs.get('montage_id')

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

class MontageClip():
    def __init__(self, **kwargs):
        self.montage_id = kwargs.get('montage_id')
        self.clip_id = kwargs.get('clip_id')
        self.clip_order = kwargs.get('clip_order')

    def is_init(self):
        init_keys = [
            'clip_order',
        ]
        return all(ik in self.__dict__ and self.__dict__[ik] is not None for ik in init_keys)

def save_montage(montage):
    if not montage.montage_id:
        montage.montage_id = f"m-{shortuuid.uuid()}"
    table_montages.put_item(Item=_replace_floats(montage.__dict__))
    _replace_decimals(montage.__dict__)
    return montage

def get_montage(montage_id):
    try:
        response = table_montages.get_item(Key={'montage_id': montage_id})
        return Montage(**_replace_decimals(response['Item']))
    except Exception as e:
        logger.warn("get_montage error", error=e)
        return None

def get_all_montages():
    try:
        response = table_montages.scan()
        return list(map(lambda c: Montage(**c), _replace_decimals(response['Items'])))
    except Exception as e:
        logger.warn("get_all_montages error", error=e)
        return []

def save_montage_clips(montage_clips):
    with table_montage_clips.batch_writer() as batch:
        for mc in montage_clips:
            batch.put_item(Item=_replace_floats(mc.__dict__))
    for mc in montage_clips:
        _replace_decimals(mc.__dict__)
    return montage_clips

def get_montage_clips(montage_id):
    try:
        response = table_montage_clips.query(
            KeyConditions={
                'montage_id': {
                    'AttributeValueList': [montage_id],
                    'ComparisonOperator': 'EQ',
                }
            }
        )
        return list(map(lambda mc: MontageClip(**mc), _replace_decimals(response['Items'])))
    except Exception as e:
        logger.warn("get_montage_clips error", error=e)
        return []

def get_montages_clips(montage_ids):
    try:
        response = table_montage_clips.scan(
            ScanFilter={
                'montage_id': {
                    'AttributeValueList': montage_ids,
                    'ComparisonOperator': 'IN',
                }
            }
        )
        return list(map(lambda mc: MontageClip(**mc), _replace_decimals(response['Items'])))
    except Exception as e:
        logger.warn("get_montages_clips error", error=e)
        return []
