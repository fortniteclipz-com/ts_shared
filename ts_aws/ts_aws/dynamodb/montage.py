import ts_config
import ts_logger
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_montages_name = ts_config.get('aws.dynamodb.montages.name')
table_montages = resource.Table(table_montages_name)

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

def save_montage(montage):
    try:
        r = table_montages.put_item(
            Item=_replace_floats(montage.__dict__),
            ReturnConsumedCapacity="TOTAL"
        )
        _replace_decimals(montage.__dict__)
        logger.info("save_montage", response=r)
    except Exception as e:
        logger.warn("save_montage error", error=e)

def get_montage(montage_id):
    try:
        r = table_montages.get_item(
            Key={'montage_id': montage_id},
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_montage", response=r)
        return Montage(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.warn("get_montage error", error=e)
        return None

def get_all_montages():
    try:
        r = table_montages.scan(
            Limit=23,
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_all_montages", response=r)
        return list(map(lambda c: Montage(**c), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_all_montages error", error=e)
        return []
