import ts_config
import ts_logger
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_streams_name = ts_config.get('aws.dynamodb.streams.name')
table_streams = resource.Table(table_streams_name)

class Stream():
    def __init__(self, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.time_offset = kwargs.get('time_offset')
        self.url_playlist_raw = kwargs.get('url_playlist_raw')

    def is_init(self):
        init_keys = [
            'time_offset',
            'url_playlist_raw',
        ]
        return all(ik in self.__dict__ and self.__dict__[ik] is not None for ik in init_keys)

def save_stream(stream):
    try:
        r = table_streams.put_item(
            Item=_replace_floats(stream.__dict__),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("save_stream", response=r)
    except Exception as e:
        logger.warn("save_stream error", error=e)

def get_stream(stream_id):
    try:
        r = table_streams.get_item(
            Key={
                'stream_id': stream_id
            },
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_stream", response=r)
        return Stream(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.warn("get_stream error", error=e)
        return None
