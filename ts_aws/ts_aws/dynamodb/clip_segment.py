import ts_config
import ts_logger
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
from boto3.dynamodb.conditions import Key, Attr

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_clip_segments_name = ts_config.get('aws.dynamodb.clip-segments.name')
table_clip_segments = resource.Table(table_clip_segments_name)

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

# good
def save_clip_segments(clip_segments):
    # try:
        with table_clip_segments.batch_writer() as batch:
            for i, cs in enumerate(clip_segments):
                r = batch.put_item(
                    Item=_replace_floats(cs.__dict__)
                )
                logger.info("save_clip_segments", current=i, total=len(clip_segments) - 1)
    # except Exception as e:
    #     logger.warn("save_clip_segments error", error=e)

# TODO: new syntax
def get_clip_segments(clip_id):
    try:
        r = table_clip_segments.query(
            KeyConditionExpression=Key('clip_id').eq(clip_id),
            ReturnConsumedCapacity="TOTAL"
        )
        return list(map(lambda cs: ClipSegment(**cs), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_clip_segments error", error=e)
        return []

# TODO: batch get
def get_clips_segments(clip_ids):
    try:
        r = table_clip_segments.scan(
            ScanFilter={
                'clip_id': {
                    'AttributeValueList': clip_ids,
                    'ComparisonOperator': 'IN',
                }
            }
        )
        return list(map(lambda cs: ClipSegment(**cs), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_clips_segments error", error=e)
        return []
