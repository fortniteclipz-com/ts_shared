import ts_config
import ts_logger

import boto3
import json

logger = ts_logger.get(__name__)

client = boto3.client('sqs')
resource = boto3.resource('sqs')

queue_name = f"{ts_config.get('sqs.queues.stream--analyze.name')}-{ts_config.get('stage')}"
queue_url = client.get_queue_url(QueueName=queue_name)['QueueUrl']
queue = resource.Queue(queue_url)

def send_message(payload):
    logger.info("send_message | start", payload=payload)
    r = queue.send_message(
        MessageBody=json.dumps(payload)
    )
    logger.info("send_message | success", response=r)

def change_visibility(receipt_handle):
    if receipt_handle is not None:
        logger.info("change_visibility | start", receipt_handle=receipt_handle)
        message = queue.Message(receipt_handle)
        r = message.change_visibility(
            VisibilityTimeout=15
        )
        logger.info("change_visibility | success", response=r)
