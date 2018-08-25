import ts_config
import ts_logger
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

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
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')
        self.url_media_raw = kwargs.get('url_media_raw')

        self.key_media_video = kwargs.get('key_media_video')
        self.key_media_audio = kwargs.get('key_media_audio')
        self.key_packets_video = kwargs.get('key_packets_video')
        self.key_packets_audio = kwargs.get('key_packets_audio')
        self.key_media_video_fresh = kwargs.get('key_media_video_fresh')
        self.key_packets_video_fresh = kwargs.get('key_packets_video_fresh')

        self._status_download = kwargs.get('_status_download')
        self._status_fresh = kwargs.get('_status_fresh')
        self._status_analyze = kwargs.get('_status_analyze')

def save_stream_segment(stream_segment):
    logger.info("save_stream_segment | start", stream_segment=stream_segment.__dict__)
    try:
        r = table_stream_segments.put_item(
            Item=_replace_floats(stream_segment.__dict__),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("save_stream_segment | success", response=r)
    except Exception as e:
            logger.error("save_stream_segment | error", error=e)

def get_stream_segment(stream_id, segment):
    logger.info("get_stream_segment | start", stream_id=stream_id, segment=segment)
    try:
        r = table_stream_segments.get_item(
            Key={
                'stream_id': stream_id,
                'segment': segment,
            },
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_stream_segment | success", response=r)
        return StreamSegment(**_replace_decimals(r['Item']))
    except Exception as e:
        logger.error("get_stream_segment | error", error=e)
        return None

def save_stream_segments(stream_segments):
    logger.info("save_stream_segments | start", stream_segments_length=len(stream_segments))
    try:
        with table_stream_segments.batch_writer() as batch:
            for i, ss in enumerate(stream_segments):
                batch.put_item(
                    Item=_replace_floats(ss.__dict__)
                )
                logger.info("save_stream_segments | success", current=i+1, total=len(stream_segments))
    except Exception as e:
        logger.error("save_stream_segments | error", error=e)

def get_stream_segments(stream_id):
    logger.info("get_stream_segments | start", stream_id=stream_id)
    try:
        r = table_stream_segments.query(
            KeyConditionExpression="stream_id = :stream_id",
            ExpressionAttributeValues=_replace_floats({
                ':stream_id': stream_id,
            }),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_stream_segments | success", response=r)
        return list(map(lambda ss: StreamSegment(**ss), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.error("get_stream_segments | error", error=e)
        return []
