import ts_config
import ts_logger

from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

from boto3.dynamodb.conditions import Key, Attr

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_stream_segments_name = ts_config.get('aws.dynamodb.stream-segments.name')
table_stream_segments = resource.Table(table_stream_segments_name)

class StreamSegment():
    def __init__(self, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')
        self.padded = kwargs.get('padded')
        self.time_duration = kwargs.get('time_duration')
        self.time_out = kwargs.get('time_out')
        self.time_in = kwargs.get('time_in')
        self.url_media_raw = kwargs.get('url_media_raw')

        self.key_media_video = kwargs.get('key_media_video')
        self.key_media_audio = kwargs.get('key_media_audio')
        self.key_packets_video = kwargs.get('key_packets_video')
        self.key_packets_audio = kwargs.get('key_packets_audio')
        self.key_media_video_fresh = kwargs.get('key_media_video_fresh')
        self.key_packets_video_fresh = kwargs.get('key_packets_video_fresh')

    def is_init_raw(self):
        raw_keys = [
            'key_media_video',
            'key_packets_video',
            'key_media_audio',
            'key_packets_audio',
        ]
        return all(rk in self.__dict__ and self.__dict__[rk] is not None for rk in raw_keys)

    def is_init_fresh(self):
        fresh_keys = [
            'key_media_video',
            'key_packets_video',
            'key_media_audio',
            'key_packets_audio',
            'key_media_video_fresh',
            'key_packets_video_fresh',
        ]
        return all(fk in self.__dict__ and self.__dict__[fk] is not None for fk in fresh_keys)

def save_stream_segment(stream_segment):
    table_stream_segments.put_item(
        Item=_replace_floats(stream_segment.__dict__),
        ReturnConsumedCapacity="TOTAL"
    )
    _replace_decimals(stream_segment.__dict__)
    return stream_segment

def get_stream_segment(stream_id, segment):
    try:
        r = table_stream_segments.get_item(
            Key={
                'stream_id': stream_id,
                'segment': segment,
            },
            ReturnConsumedCapacity="TOTAL"
        )
        return StreamSegment(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.warn("get_stream_segment error", error=e)
        return None

def save_stream_segments(stream_segments):
    with table_stream_segments.batch_writer() as batch:
        for ss in stream_segments:
            batch.put_item(
                Item=_replace_floats(ss.__dict__),
                ReturnConsumedCapacity="TOTAL"
            )
    return list(map(lambda ss: StreamSegment(**_replace_decimals(ss.__dict__)), stream_segments))

# TODO: new syntax
def get_stream_segments(stream_id):
    try:
        r = table_stream_segments.query(
            KeyConditionExpression=Key('stream_id').eq(stream_id),
            Limit=10,
            ReturnConsumedCapacity="TOTAL"
        )
        print(f"\n{r}\n")
        return list(map(lambda ss: StreamSegment(**ss), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_stream_segments error", error=e)
        return []
