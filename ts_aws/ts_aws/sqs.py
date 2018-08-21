import ts_config

import boto3
import json

client = boto3.client('sqs')
resource = boto3.resource('sqs')

stream_segment_queue_url = client.get_queue_url(QueueName=ts_config.get('aws.sqs.stream-segment.name'))['QueueUrl']
stream_segment_queue = resource.Queue(stream_segment_queue_url)

clip_queue_url = client.get_queue_url(QueueName=ts_config.get('aws.sqs.clip.name'))['QueueUrl']
clip_queue = resource.Queue(clip_queue_url)

def send_stream_download(payload):
    stream_segment_queue.send_message(MessageBody=json.dumps(payload))

def send_stream_clip(payload):
    clip_queue.send_message(MessageBody=json.dumps(payload))
