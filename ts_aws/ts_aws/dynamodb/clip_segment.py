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
    try:
        with table_clip_segments.batch_writer() as batch:
            for i, cs in enumerate(clip_segments):
                batch.put_item(
                    Item=_replace_floats(cs.__dict__)
                )
                logger.info("save_clip_segments | success", current=i+1, total=len(clip_segments))
    except Exception as e:
        logger.error("save_clip_segments | error", error=e)

def get_clip_segments(clip_id):
    logger.info("get_clip_segments | start", clip_id=clip_id)
    try:
        r = table_clip_segments.query(
            KeyConditionExpression="clip_id = :clip_id",
            ExpressionAttributeValues=_replace_floats({
                ':clip_id': clip_id,
            }),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_clip_segments | success", response=r)
        return list(map(lambda cs: ts_model.ClipSegment(**cs), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.error("get_clip_segments | error", error=e)
        return []

def get_clips_segments(clip_ids):
    logger.info("get_clips_segments | start", clip_ids=clip_ids)
    clip_segments = []
    try:
        for c_id in clip_ids:
            r = table_clip_segments.query(
                KeyConditionExpression="clip_id = :clip_id",
                ExpressionAttributeValues=_replace_floats({
                    ':clip_id': c_id,
                }),
                ReturnConsumedCapacity="TOTAL"
            )
            logger.info("get_clips_segments | success", clip_id=c_id, response=r)
            clip_segments += list(map(lambda cs: ts_model.ClipSegment(**cs), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.error("get_clips_segments | error", error=e)
    finally:
        return clip_segments
