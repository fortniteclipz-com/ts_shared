import ts_config
import ts_logger

import boto3
import json

logger = ts_logger.get(__name__)

client = boto3.client('sqs')
resource = boto3.resource('sqs')

queue_url = client.get_queue_url(QueueName=ts_config.get('aws.sqs.stream-segment--download.name'))['QueueUrl']
queue = resource.Queue(queue_url)

def send_message(payload):
    logger.info("send_message | start", payload=payload)
    r = queue.send_message(
        MessageBody=json.dumps(payload)
    )
    logger.info("send_message | success", response=r)

def send_messages(payloads):
    logger.info("send_messages | start", payloads=payloads)
    r = queue.send_messages(
        Entries=list(map(lambda p: {
            'Id': f"{p['stream_id']}-{p['segment']}",
            'MessageBody': json.dumps(p),
        }, payloads))
    )
    logger.info("send_messages | success", response=r)

def change_visibility(receipt_handle):
    if receipt_handle is not None:
        logger.info("change_visibility | start", receipt_handle=receipt_handle)
        message = queue.Message(receipt_handle)
        r = message.change_visibility(
            VisibilityTimeout=15
        )
        logger.info("change_visibility | success", response=r)
