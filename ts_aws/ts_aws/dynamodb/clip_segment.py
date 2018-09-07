import ts_config
import ts_logger
import ts_model.ClipSegment
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_clip_segments_name = ts_config.get('aws.dynamodb.clip-segments.name')
table_clip_segments = resource.Table(table_clip_segments_name)

def save_clip_segments(clip_segments):
    logger.info("save_clip_segments | start", clip_segments_length=len(clip_segments))
    with table_clip_segments.batch_writer() as batch:
        for cs in clip_segments:
            batch.put_item(
                Item=_replace_floats(cs),
            )
    logger.info("save_clip_segments | success")

