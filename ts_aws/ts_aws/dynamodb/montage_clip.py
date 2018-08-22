import ts_config
import ts_logger
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_montage_clips_name = ts_config.get('aws.dynamodb.montage-clips.name')
table_montage_clips = resource.Table(table_montage_clips_name)

class MontageClip():
    def __init__(self, **kwargs):
        self.montage_id = kwargs.get('montage_id')
        self.clip_id = kwargs.get('clip_id')
        self.clip_order = kwargs.get('clip_order')

def save_montage_clips(montage_clips):
    try:
        with table_montage_clips.batch_writer() as batch:
            for i, mc in enumerate(montage_clips):
                batch.put_item(
                    Item=_replace_floats(mc.__dict__)
                )
                logger.info("save_montage_clips", current=i+1, total=len(montage_clips))
        return list(map(lambda mc: MontageClip(**_replace_decimals(mc.__dict__)), montage_clips))
    except Exception as e:
        logger.warn("save_montage_clips error", error=e)

def get_montage_clips(montage_id):
    try:
        r = table_montage_clips.query(
            KeyConditionExpression="montage_id = :montage_id",
            ExpressionAttributeValues=_replace_floats({
                ':montage_id': montage_id,
            }),
            ReturnConsumedCapacity="TOTAL"
        )
        logger.info("get_montage_clips", response=r)
        return list(map(lambda mc: MontageClip(**mc), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_montage_clips error", error=e)
        return []
