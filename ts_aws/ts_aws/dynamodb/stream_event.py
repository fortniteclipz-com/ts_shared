import ts_config
import ts_logger
import ts_model.StreamEvent
from ts_aws.dynamodb import _replace_decimals, _replace_floats

import boto3

logger = ts_logger.get(__name__)

resource = boto3.resource('dynamodb')
table_stream_events_name = ts_config.get('aws.dynamodb.stream-events.name')
table_stream_events = resource.Table(table_stream_events_name)

def save_stream_events(stream_events):
    logger.info("save_stream_events | start", stream_events_length=len(stream_events))
    with table_stream_events.batch_writer() as batch:
        for i, ss in enumerate(stream_events):
            batch.put_item(
                Item=_replace_floats(ss),
            )
    logger.info("save_stream_events | success")
