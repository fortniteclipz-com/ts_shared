import ts_config
import ts_logger
import ts_model.MontageClip
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3
import traceback

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_montage_clips_name = ts_config.get('aws.dynamodb.montage-clips.name')
table_montage_clips = resource.Table(table_montage_clips_name)

def save_montage_clips(montage_clips):
    logger.info("save_montage_clips | start", montage_clips_length=len(montage_clips))
    with table_montage_clips.batch_writer() as batch:
        for i, mc in enumerate(montage_clips):
            batch.put_item(
                Item=_replace_floats(mc)
            )
    logger.info("save_montage_clips | success")
    return list(map(lambda mc: ts_model.MontageClip(**_replace_decimals(mc)), montage_clips))

def get_montage_clips(montage_id):
    logger.info("get_montage_clips | start", montage_id=montage_id)
    r = table_montage_clips.query(
        KeyConditionExpression="montage_id = :montage_id",
        ExpressionAttributeValues=_replace_floats({
            ':montage_id': montage_id,
        }),
        ReturnConsumedCapacity="TOTAL"
    )
    logger.info("get_montage_clips | success", response=r)
    return list(map(lambda mc: ts_model.MontageClip(**mc), _replace_decimals(r['Items'])))
