import ts_config

import boto3
import json

client = boto3.client('sqs')
resource = boto3.resource('sqs')

stream_segment_queue_name = ts_config.get('aws.sqs.stream-segment.name')
response = client.get_queue_url(QueueName=stream_segment_queue_name)
stream_segment_queue_url = response['QueueUrl']
stream_segment_queue = resource.Queue(stream_segment_queue_url)

clip_queue_name = ts_config.get('aws.sqs.clip.name')
response = client.get_queue_url(QueueName=clip_queue_name)
clip_queue_url = response['QueueUrl']
clip_queue = resource.Queue(clip_queue_url)

def send_stream_download(payload):
    stream_segment_queue.send_message(MessageBody=json.dumps(payload))

def send_stream_clip(payload):
    clip_queue.send_message(MessageBody=json.dumps(payload))
