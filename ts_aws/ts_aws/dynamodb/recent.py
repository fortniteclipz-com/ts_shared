import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Recent
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

stage = ts_config.get('stage')
resource = boto3.resource('dynamodb')
table_recents_name = f"{ts_config.get('dynamodb.tables.streams.name')}-{stage}"
table_recents = resource.Table(table_recents_name)

def save_streams():
    pass

def get_streams():
    pass

def save_montages():
    pass

def get_montages():
    pass
