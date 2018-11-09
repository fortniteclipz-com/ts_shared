import ts_config
import ts_logger
import ts_model.Clip
import ts_model.ClipSegment
import ts_model.Exception
import ts_model.StreamSegment
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_clips_name = f"{ts_config.get('dynamodb.tables.clips.name')}-{stage}"
table_clips = resource.Table(table_clips_name)
table_stream_segments_name = f"{ts_config.get('dynamodb.tables.stream-segments.name')}-{stage}"
table_stream_segments = resource.Table(table_stream_segments_name)

def save_clip(clip):
    logger.info("save_clip | start", clip=clip)
    r = table_clips.put_item(
        Item=_replace_floats(clip),
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("save_clip | success", response=r)

def get_clip(clip_id):
    logger.info("get_clip | start", clip_id=clip_id)
    r = table_clips.get_item(
        Key={
            'clip_id': clip_id,
        },
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_clip | success", response=r)
    if 'Item' not in r:
        raise ts_model.Exception(ts_model.Exception.CLIP__NOT_EXIST)
    return ts_model.Clip(**_replace_decimals(r['Item']))

def save_clips(clips):
    logger.info("save_clips | start", clips_length=len(clips))
    with table_clips.batch_writer() as batch:
        for c in clips:
            batch.put_item(
                Item=_replace_floats(c),
            )
    logger.info("save_clips | success")

def get_clips(clip_ids):
    logger.info("get_clips | start", clip_ids=clip_ids)
    r = resource.batch_get_item(
        RequestItems={
            table_clips_name: {
                'Keys': list(map(lambda c_id: {'clip_id': c_id}, clip_ids)),
            }
        },
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_clips | success", response=r)
    if len(r['Responses'][table_clips_name]) == 0:
            raise ts_model.Exception(ts_model.Exception.CLIPS__NOT_EXIST)
    return list(map(lambda c: ts_model.Clip(**c), _replace_decimals(r['Responses'][table_clips_name])))

def get_all_clips(limit):
    logger.info("get_all_clips | start", limit=limit)
    r = table_clips.scan(
        Limit=limit,
        ReturnConsumedCapacity='TOTAL',
    )
    logger.info("get_all_clips | success", response=r)
    return list(map(lambda c: ts_model.Clip(**c), _replace_decimals(r['Items'])))
