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

    def is_init(self):
        init_keys = [
            'clip_order',
        ]
        return all(ik in self.__dict__ and self.__dict__[ik] is not None for ik in init_keys)

def save_montage_clips(montage_clips):
    with table_montage_clips.batch_writer() as batch:
        for mc in montage_clips:
            batch.put_item(Item=_replace_floats(mc.__dict__))
    return list(map(lambda mc: MontageClip(**_replace_decimals(mc.__dict__)), montage_clips))

# TODO: new syntax
def get_montage_clips(montage_id):
    try:
        r = table_montage_clips.query(
            KeyConditions={
                'montage_id': {
                    'AttributeValueList': [montage_id],
                    'ComparisonOperator': 'EQ',
                }
            }
        )
        return list(map(lambda mc: MontageClip(**mc), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_montage_clips error", error=e)
        return []

# TODO: query
def get_montages_clips(montage_ids):
    try:
        r = table_montage_clips.scan(
            ScanFilter={
                'montage_id': {
                    'AttributeValueList': montage_ids,
                    'ComparisonOperator': 'IN',
                }
            }
        )
        return list(map(lambda mc: MontageClip(**mc), _replace_decimals(r['Items'])))
    except Exception as e:
        logger.warn("get_montages_clips error", error=e)
        return []
