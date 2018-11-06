import ts_config
import ts_logger
import ts_model.UserClip
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_user_clips_name = f"{ts_config.get('dynamodb.tables.user-clips.name')}-{stage}"
table_user_clips = resource.Table(table_user_clips_name)

def save_user_clips(user_clips):
    logger.info("save_user_clips | start", user_clips_length=len(user_clips))
    with table_user_clips.batch_writer() as batch:
        for uc in user_clips:
            batch.put_item(
                Item=_replace_floats(uc),
            )
    logger.info("save_user_clips | success")

