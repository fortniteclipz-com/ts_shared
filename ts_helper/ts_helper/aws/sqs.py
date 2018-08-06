import ts_config

import boto3
import json

client = boto3.client('sqs')
resource = boto3.resource('sqs')

stream_download_name = ts_config.get('aws.sqs.stream-download.name')
response = client.get_queue_url(QueueName=stream_download_name)
queue_stream_download_url = response['QueueUrl']
queue_stream_download = resource.Queue(queue_stream_download_url)

stream_clip_name = ts_config.get('aws.sqs.stream-clip.name')
response = client.get_queue_url(QueueName=stream_clip_name)
queue_stream_clip_url = response['QueueUrl']
queue_stream_clip = resource.Queue(queue_stream_clip_url)

clips_montage_name = ts_config.get('aws.sqs.clips-montage.name')
response = client.get_queue_url(QueueName=clips_montage_name)
queue_clips_montage_url = response['QueueUrl']
queue_clips_montage = resource.Queue(queue_clips_montage_url)

def send_stream_download(payload):
    queue_stream_download.send_message(MessageBody=json.dumps(payload))

def send_stream_clip(payload):
    queue_stream_clip.send_message(MessageBody=json.dumps(payload))

def send_clips_montage(payload):
    queue_clips_montage.send_message(MessageBody=json.dumps(payload))

