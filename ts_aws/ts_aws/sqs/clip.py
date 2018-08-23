import ts_config

import boto3
import json

client = boto3.client('sqs')
resource = boto3.resource('sqs')

queue_url = client.get_queue_url(QueueName=ts_config.get('aws.sqs.clip.name'))['QueueUrl']
queue = resource.Queue(queue_url)

def send_message(payload):
    queue.send_message(MessageBody=json.dumps(payload))

def change_visibility(receipt_handle):
    message = queue.Message(receipt_handle)
    message.change_visibility(VisibilityTimeout=15)
