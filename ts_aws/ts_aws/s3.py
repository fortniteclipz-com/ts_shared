import ts_config

import boto3
import json
import os

resource = boto3.resource('s3')
bucket_main = resource.Bucket(ts_config.get('aws.s3.main.name'))

def upload_file(filename, s3_key):
    bucket_main.upload_file(filename, s3_key)

def download_file(s3_key, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    body = bucket_main.download_file(s3_key, filename)
